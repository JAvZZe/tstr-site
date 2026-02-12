


SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


COMMENT ON SCHEMA "public" IS 'standard public schema';



CREATE EXTENSION IF NOT EXISTS "hypopg" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "index_advisor" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "pg_graphql" WITH SCHEMA "graphql";






CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "pgcrypto" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "supabase_vault" WITH SCHEMA "vault";






CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "wrappers" WITH SCHEMA "extensions";






CREATE OR REPLACE FUNCTION "public"."can_auto_claim"("user_email" "text", "listing_website" "text") RETURNS boolean
    LANGUAGE "plpgsql" IMMUTABLE
    SET "search_path" TO 'pg_catalog', 'public'
    AS $_$
DECLARE
  user_domain TEXT;
  listing_domain TEXT;
BEGIN
  IF user_email IS NULL OR listing_website IS NULL THEN
    RETURN FALSE;
  END IF;

  -- Extract domain from email
  user_domain := split_part(user_email, '@', 2);
  IF user_domain IS NULL THEN
    RETURN FALSE;
  END IF;

  -- Extract domain from website
  listing_domain := extract_domain(listing_website);
  IF listing_domain IS NULL THEN
    RETURN FALSE;
  END IF;

  -- Exact match
  IF lower(user_domain) = lower(listing_domain) THEN
    RETURN TRUE;
  END IF;

  -- Handle common TLD variations (optional enhancement)
  user_domain := regexp_replace(lower(user_domain), '\.(com|org|net|edu|gov)$', '');
  listing_domain := regexp_replace(lower(listing_domain), '\.(com|org|net|edu|gov)$', '');

  RETURN user_domain = listing_domain;
END;
$_$;


ALTER FUNCTION "public"."can_auto_claim"("user_email" "text", "listing_website" "text") OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."can_view_contact_info"("user_uuid" "uuid") RETURNS boolean
    LANGUAGE "sql" STABLE
    SET "search_path" TO 'pg_catalog', 'public'
    AS $$
  SELECT subscription_tier IN ('professional', 'premium', 'enterprise')
  FROM user_profiles
  WHERE id = user_uuid;
$$;


ALTER FUNCTION "public"."can_view_contact_info"("user_uuid" "uuid") OWNER TO "postgres";


COMMENT ON FUNCTION "public"."can_view_contact_info"("user_uuid" "uuid") IS 'Returns TRUE if user tier allows viewing phone/email';



CREATE OR REPLACE FUNCTION "public"."extract_domain"("url" "text") RETURNS "text"
    LANGUAGE "plpgsql" IMMUTABLE
    SET "search_path" TO 'pg_catalog', 'public'
    AS $$
BEGIN
  IF url IS NULL OR url = '' THEN
    RETURN NULL;
  END IF;

  -- Remove protocol
  url := regexp_replace(url, '^https?://', '');

  -- Remove www prefix
  url := regexp_replace(url, '^www\.', '');

  -- Extract domain (everything before first / or ?)
  url := split_part(url, '/', 1);
  url := split_part(url, '?', 1);
  url := split_part(url, '#', 1);

  RETURN lower(trim(url));
END;
$$;


ALTER FUNCTION "public"."extract_domain"("url" "text") OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."get_click_stats"("days_back" integer DEFAULT 30) RETURNS TABLE("date" "date", "clicks" bigint, "unique_listings" bigint)
    LANGUAGE "sql" STABLE
    SET "search_path" TO 'pg_catalog', 'public'
    AS $$
  SELECT
    DATE(created_at) as date,
    COUNT(*) as clicks,
    COUNT(DISTINCT listing_id) as unique_listings
  FROM clicks
  WHERE created_at >= NOW() - (days_back || ' days')::INTERVAL
  GROUP BY DATE(created_at)
  ORDER BY date DESC;
$$;


ALTER FUNCTION "public"."get_click_stats"("days_back" integer) OWNER TO "postgres";


COMMENT ON FUNCTION "public"."get_click_stats"("days_back" integer) IS 'Returns daily click statistics for the last N days';



CREATE OR REPLACE FUNCTION "public"."get_top_clicked_listings"("limit_count" integer DEFAULT 10) RETURNS TABLE("listing_id" "uuid", "business_name" "text", "website" "text", "category_name" "text", "clicks" bigint, "last_click" timestamp with time zone)
    LANGUAGE "sql" STABLE
    SET "search_path" TO 'pg_catalog', 'public'
    AS $$
  SELECT
    l.id as listing_id,
    l.business_name,
    l.website,
    c.name as category_name,
    COUNT(cl.id) as clicks,
    MAX(cl.created_at) as last_click
  FROM clicks cl
  JOIN listings l ON cl.listing_id = l.id
  LEFT JOIN categories c ON l.category_id = c.id
  GROUP BY l.id, l.business_name, l.website, c.name
  ORDER BY clicks DESC, last_click DESC
  LIMIT limit_count;
$$;


ALTER FUNCTION "public"."get_top_clicked_listings"("limit_count" integer) OWNER TO "postgres";


COMMENT ON FUNCTION "public"."get_top_clicked_listings"("limit_count" integer) IS 'Returns top N listings by click count with aggregated metrics';



CREATE OR REPLACE FUNCTION "public"."get_user_tier"("user_uuid" "uuid") RETURNS "text"
    LANGUAGE "sql" STABLE
    SET "search_path" TO 'pg_catalog', 'public'
    AS $$
  SELECT COALESCE(subscription_tier, 'free')
  FROM user_profiles
  WHERE id = user_uuid;
$$;


ALTER FUNCTION "public"."get_user_tier"("user_uuid" "uuid") OWNER TO "postgres";


COMMENT ON FUNCTION "public"."get_user_tier"("user_uuid" "uuid") IS 'Returns subscription tier for a user (returns free if no profile exists)';



CREATE OR REPLACE FUNCTION "public"."handle_new_user"() RETURNS "trigger"
    LANGUAGE "plpgsql" SECURITY DEFINER
    SET "search_path" TO 'pg_catalog', 'public'
    AS $$
BEGIN
  INSERT INTO public.user_profiles (id, billing_email, subscription_tier, role)
  VALUES (
    NEW.id,
    NEW.email,
    'free',
    'user'
  );
  RETURN NEW;
END;
$$;


ALTER FUNCTION "public"."handle_new_user"() OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."make_user_admin"("user_email" "text") RETURNS boolean
    LANGUAGE "plpgsql" SECURITY DEFINER
    SET "search_path" TO 'pg_catalog', 'public'
    AS $$
BEGIN
  UPDATE user_profiles
  SET role = 'admin'
  WHERE billing_email = user_email;

  RETURN FOUND;
END;
$$;


ALTER FUNCTION "public"."make_user_admin"("user_email" "text") OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."search_by_standard"("p_standard_code" "text", "p_category_id" "uuid" DEFAULT NULL::"uuid", "p_min_specs" "jsonb" DEFAULT '{}'::"jsonb") RETURNS TABLE("listing_id" "uuid", "business_name" "text", "website" "text", "standard_code" "text", "standard_name" "text", "specifications" "jsonb")
    LANGUAGE "plpgsql" STABLE
    SET "search_path" TO 'pg_catalog', 'public'
    AS $$
BEGIN
  RETURN QUERY
  SELECT 
    l.id AS listing_id,
    l.business_name,
    l.website,
    s.code AS standard_code,
    s.name AS standard_name,
    lc.specifications
  FROM listings l
  JOIN listing_capabilities lc ON l.id = lc.listing_id
  JOIN standards s ON lc.standard_id = s.id
  WHERE 
    s.code = p_standard_code
    AND (p_category_id IS NULL OR l.category_id = p_category_id)
    AND l.status = 'active'
    AND lc.specifications @> p_min_specs  -- JSONB contains operator
  ORDER BY 
    lc.verified DESC,  -- Verified capabilities first
    l.is_featured DESC,
    l.created_at DESC;
END;
$$;


ALTER FUNCTION "public"."search_by_standard"("p_standard_code" "text", "p_category_id" "uuid", "p_min_specs" "jsonb") OWNER TO "postgres";


COMMENT ON FUNCTION "public"."search_by_standard"("p_standard_code" "text", "p_category_id" "uuid", "p_min_specs" "jsonb") IS 'Search listings by standard code with optional technical specification filters';



CREATE OR REPLACE FUNCTION "public"."update_updated_at_column"() RETURNS "trigger"
    LANGUAGE "plpgsql"
    SET "search_path" TO 'pg_catalog', 'public'
    AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;


ALTER FUNCTION "public"."update_updated_at_column"() OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."update_website_domain"() RETURNS "trigger"
    LANGUAGE "plpgsql"
    SET "search_path" TO 'pg_catalog', 'public'
    AS $$
BEGIN
  IF NEW.website IS DISTINCT FROM OLD.website THEN
    NEW.website_domain := extract_domain(NEW.website);
  END IF;
  RETURN NEW;
END;
$$;


ALTER FUNCTION "public"."update_website_domain"() OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."user_owns_listing"("user_uuid" "uuid", "listing_uuid" "uuid") RETURNS boolean
    LANGUAGE "sql" STABLE
    SET "search_path" TO 'pg_catalog', 'public'
    AS $$
  SELECT EXISTS (
    SELECT 1
    FROM listing_ownership
    WHERE user_id = user_uuid
      AND listing_id = listing_uuid
      AND verified_owner = TRUE
  );
$$;


ALTER FUNCTION "public"."user_owns_listing"("user_uuid" "uuid", "listing_uuid" "uuid") OWNER TO "postgres";


COMMENT ON FUNCTION "public"."user_owns_listing"("user_uuid" "uuid", "listing_uuid" "uuid") IS 'Returns TRUE if user is verified owner of listing';


SET default_tablespace = '';

SET default_table_access_method = "heap";


CREATE TABLE IF NOT EXISTS "public"."categories" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "name" "text" NOT NULL,
    "slug" "text" NOT NULL,
    "parent_id" "uuid",
    "description" "text",
    "icon" "text",
    "display_order" integer DEFAULT 0,
    "created_at" timestamp with time zone DEFAULT "now"(),
    "updated_at" timestamp with time zone DEFAULT "now"()
);


ALTER TABLE "public"."categories" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."claims" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "provider_name" "text" NOT NULL,
    "contact_name" "text" NOT NULL,
    "business_email" "text" NOT NULL,
    "phone" "text",
    "status" "text" DEFAULT 'pending'::"text",
    "created_at" timestamp with time zone DEFAULT "now"(),
    "updated_at" timestamp with time zone DEFAULT "now"(),
    CONSTRAINT "claims_status_check" CHECK (("status" = ANY (ARRAY['pending'::"text", 'verified'::"text", 'rejected'::"text"])))
);


ALTER TABLE "public"."claims" OWNER TO "postgres";


COMMENT ON TABLE "public"."claims" IS 'Stores provider ownership claim 
     requests for listing verification';



COMMENT ON COLUMN "public"."claims"."business_email" IS 'Business email used for
      domain verification';



COMMENT ON COLUMN "public"."claims"."status" IS 'Claim status: pending (awaiting
      verification), verified (approved), rejected (denied)';



CREATE TABLE IF NOT EXISTS "public"."clicks" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "listing_id" "uuid",
    "url" "text" NOT NULL,
    "user_agent" "text",
    "referrer" "text",
    "created_at" timestamp with time zone DEFAULT "now"()
);


ALTER TABLE "public"."clicks" OWNER TO "postgres";


COMMENT ON TABLE "public"."clicks" IS 'Tracks outbound clicks to listing websites. Used for engagement analytics and dead link detection.';



CREATE TABLE IF NOT EXISTS "public"."custom_fields" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "category_id" "uuid",
    "field_name" "text" NOT NULL,
    "field_label" "text" NOT NULL,
    "field_type" "text" NOT NULL,
    "options" "jsonb",
    "is_required" boolean DEFAULT false,
    "is_searchable" boolean DEFAULT true,
    "display_order" integer DEFAULT 0,
    "created_at" timestamp with time zone DEFAULT "now"(),
    CONSTRAINT "custom_fields_field_type_check" CHECK (("field_type" = ANY (ARRAY['text'::"text", 'number'::"text", 'boolean'::"text", 'select'::"text", 'multi_select'::"text", 'date'::"text", 'url'::"text"])))
);


ALTER TABLE "public"."custom_fields" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."listing_capabilities" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "listing_id" "uuid" NOT NULL,
    "standard_id" "uuid" NOT NULL,
    "specifications" "jsonb" DEFAULT '{}'::"jsonb",
    "verified" boolean DEFAULT false,
    "verified_at" timestamp with time zone,
    "verified_by" "uuid",
    "notes" "text",
    "display_order" integer DEFAULT 0,
    "created_at" timestamp with time zone DEFAULT "now"(),
    "updated_at" timestamp with time zone DEFAULT "now"()
);


ALTER TABLE "public"."listing_capabilities" OWNER TO "postgres";


COMMENT ON TABLE "public"."listing_capabilities" IS 'Links listings to standards they can perform, with technical specifications';



COMMENT ON COLUMN "public"."listing_capabilities"."specifications" IS 'Flexible JSONB field for category-specific technical metadata';



CREATE TABLE IF NOT EXISTS "public"."listing_categories" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "listing_id" "uuid",
    "category_id" "uuid",
    "is_primary" boolean DEFAULT false,
    "created_at" timestamp with time zone DEFAULT "now"()
);


ALTER TABLE "public"."listing_categories" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."listing_custom_fields" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "listing_id" "uuid",
    "custom_field_id" "uuid",
    "value" "jsonb" NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"()
);


ALTER TABLE "public"."listing_custom_fields" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."listing_images" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "listing_id" "uuid",
    "image_url" "text" NOT NULL,
    "is_primary" boolean DEFAULT false,
    "display_order" integer DEFAULT 0,
    "created_at" timestamp with time zone DEFAULT "now"()
);


ALTER TABLE "public"."listing_images" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."listing_owners" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "user_id" "uuid" NOT NULL,
    "listing_id" "uuid" NOT NULL,
    "role" "text" DEFAULT 'owner'::"text" NOT NULL,
    "status" "text" DEFAULT 'pending'::"text" NOT NULL,
    "verification_method" "text",
    "verified_at" timestamp with time zone,
    "verification_token" "text",
    "token_expires_at" timestamp with time zone,
    "created_at" timestamp with time zone DEFAULT "now"(),
    "updated_at" timestamp with time zone DEFAULT "now"(),
    CONSTRAINT "listing_owners_role_check" CHECK (("role" = ANY (ARRAY['owner'::"text", 'editor'::"text", 'admin'::"text"]))),
    CONSTRAINT "listing_owners_status_check" CHECK (("status" = ANY (ARRAY['pending'::"text", 'verified'::"text", 'rejected'::"text"]))),
    CONSTRAINT "listing_owners_verification_method_check" CHECK (("verification_method" = ANY (ARRAY['domain_match'::"text", 'email_verification'::"text", 'admin_approval'::"text"])))
);


ALTER TABLE "public"."listing_owners" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."listing_ownership" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "listing_id" "uuid" NOT NULL,
    "user_id" "uuid" NOT NULL,
    "claimed_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "verified_owner" boolean DEFAULT false NOT NULL,
    "verification_method" "text",
    "verified_at" timestamp with time zone,
    "verified_by" "uuid",
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    CONSTRAINT "listing_ownership_verification_method_check" CHECK (("verification_method" = ANY (ARRAY['email_domain'::"text", 'manual'::"text", 'document'::"text"])))
);


ALTER TABLE "public"."listing_ownership" OWNER TO "postgres";


COMMENT ON TABLE "public"."listing_ownership" IS 'Tracks which users own/manage which listings';



COMMENT ON COLUMN "public"."listing_ownership"."verified_owner" IS 'TRUE if ownership has been verified by admin';



CREATE TABLE IF NOT EXISTS "public"."listings" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "owner_id" "uuid",
    "category_id" "uuid" NOT NULL,
    "location_id" "uuid" NOT NULL,
    "business_name" "text" NOT NULL,
    "slug" "text" NOT NULL,
    "description" "text",
    "website" "text",
    "email" "text",
    "phone" "text",
    "address" "text",
    "latitude" numeric(10,8),
    "longitude" numeric(11,8),
    "plan_type" "text" DEFAULT 'free'::"text",
    "is_featured" boolean DEFAULT false,
    "featured_until" timestamp with time zone,
    "status" "text" DEFAULT 'pending'::"text",
    "verified" boolean DEFAULT false,
    "claimed" boolean DEFAULT false,
    "views" integer DEFAULT 0,
    "created_at" timestamp with time zone DEFAULT "now"(),
    "updated_at" timestamp with time zone DEFAULT "now"(),
    "published_at" timestamp with time zone,
    "featured" boolean DEFAULT false NOT NULL,
    "priority_rank" integer DEFAULT 0 NOT NULL,
    "region" "text" DEFAULT 'global'::"text",
    "claimed_at" timestamp with time zone,
    "website_domain" "text",
    "contact_email" "text",
    "source_script" "text",
    "script_location" "text",
    "parent_listing_id" "uuid",
    "billing_tier" "text" DEFAULT 'free'::"text",
    CONSTRAINT "listings_billing_tier_check" CHECK (("billing_tier" = ANY (ARRAY['free'::"text", 'pro'::"text", 'enterprise'::"text"]))),
    CONSTRAINT "listings_plan_type_check" CHECK (("plan_type" = ANY (ARRAY['free'::"text", 'basic'::"text", 'featured'::"text", 'premium'::"text"]))),
    CONSTRAINT "listings_status_check" CHECK (("status" = ANY (ARRAY['pending'::"text", 'active'::"text", 'expired'::"text", 'suspended'::"text"])))
);


ALTER TABLE "public"."listings" OWNER TO "postgres";


COMMENT ON COLUMN "public"."listings"."featured" IS 'TRUE if listing should show featured badge (Premium+ tier)';



COMMENT ON COLUMN "public"."listings"."priority_rank" IS 'Priority ranking for search results (higher = appears first). Premium tier gets priority_rank > 0';



COMMENT ON COLUMN "public"."listings"."region" IS 'Geographic region of the listing (e.g., usa, eu, apac, global)';



COMMENT ON COLUMN "public"."listings"."source_script" IS 'Name of the scraper script that created this listing (e.g., oil_gas_playwright.py)';



COMMENT ON COLUMN "public"."listings"."script_location" IS 'File path or location of the scraper script (e.g., web/tstr-automation/scrapers/)';



CREATE TABLE IF NOT EXISTS "public"."locations" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "name" "text" NOT NULL,
    "slug" "text" NOT NULL,
    "parent_id" "uuid",
    "level" "text" NOT NULL,
    "latitude" numeric(10,8),
    "longitude" numeric(11,8),
    "created_at" timestamp with time zone DEFAULT "now"(),
    "updated_at" timestamp with time zone DEFAULT "now"(),
    CONSTRAINT "locations_level_check" CHECK (("level" = ANY (ARRAY['global'::"text", 'region'::"text", 'country'::"text", 'city'::"text"])))
);


ALTER TABLE "public"."locations" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."payment_history" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "user_id" "uuid",
    "amount" numeric(10,2) NOT NULL,
    "currency" "text" DEFAULT 'USD'::"text",
    "status" "text" NOT NULL,
    "paypal_transaction_id" "text",
    "paypal_subscription_id" "text",
    "tier" "text" NOT NULL,
    "description" "text",
    "created_at" timestamp with time zone DEFAULT "now"(),
    CONSTRAINT "payment_history_status_check" CHECK (("status" = ANY (ARRAY['completed'::"text", 'pending'::"text", 'failed'::"text", 'refunded'::"text"])))
);


ALTER TABLE "public"."payment_history" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."payments" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "listing_id" "uuid",
    "owner_id" "uuid",
    "amount" numeric(10,2) NOT NULL,
    "currency" "text" DEFAULT 'GBP'::"text",
    "payment_method" "text",
    "reference_number" "text",
    "proof_image_url" "text",
    "status" "text" DEFAULT 'pending'::"text",
    "verified_by" "uuid",
    "verified_at" timestamp with time zone,
    "notes" "text",
    "created_at" timestamp with time zone DEFAULT "now"(),
    CONSTRAINT "payments_payment_method_check" CHECK (("payment_method" = ANY (ARRAY['bank_transfer'::"text", 'paypal'::"text", 'bitcoin'::"text", 'stripe'::"text"]))),
    CONSTRAINT "payments_status_check" CHECK (("status" = ANY (ARRAY['pending'::"text", 'verified'::"text", 'rejected'::"text", 'refunded'::"text"])))
);


ALTER TABLE "public"."payments" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."pending_research" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "business_name" "text" NOT NULL,
    "website" "text",
    "validation_error" "text",
    "original_id" "uuid",
    "category" "text",
    "location_id" "uuid",
    "address" "text",
    "phone" "text",
    "email" "text",
    "description" "text",
    "status" "text" DEFAULT 'pending_research'::"text",
    "notes" "text",
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "researched_at" timestamp with time zone,
    "researched_by" "text"
);


ALTER TABLE "public"."pending_research" OWNER TO "postgres";


CREATE OR REPLACE VIEW "public"."potential_dead_links" WITH ("security_invoker"='true') AS
 SELECT "l"."id",
    "l"."business_name",
    "l"."website",
    "c"."name" AS "category",
    "count"("cl"."id") AS "click_attempts",
    "max"("cl"."created_at") AS "last_attempt",
    "l"."status"
   FROM (("public"."listings" "l"
     LEFT JOIN "public"."clicks" "cl" ON (("l"."id" = "cl"."listing_id")))
     LEFT JOIN "public"."categories" "c" ON (("l"."category_id" = "c"."id")))
  WHERE ("l"."website" IS NOT NULL)
  GROUP BY "l"."id", "l"."business_name", "l"."website", "c"."name", "l"."status"
 HAVING ("count"("cl"."id") > 0)
  ORDER BY ("count"("cl"."id")) DESC;


ALTER VIEW "public"."potential_dead_links" OWNER TO "postgres";


COMMENT ON VIEW "public"."potential_dead_links" IS 'Listings with clicks - useful for monitoring and dead link detection';



CREATE TABLE IF NOT EXISTS "public"."schema_migrations" (
    "version" integer NOT NULL,
    "name" "text" NOT NULL,
    "applied_at" timestamp with time zone DEFAULT "now"() NOT NULL
);


ALTER TABLE "public"."schema_migrations" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."search_logs" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "query" "text",
    "filters" "jsonb",
    "results_count" integer,
    "ip_hash" "text",
    "created_at" timestamp with time zone DEFAULT "now"()
);


ALTER TABLE "public"."search_logs" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."standards" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "code" "text" NOT NULL,
    "name" "text" NOT NULL,
    "description" "text",
    "issuing_body" "text",
    "category_id" "uuid",
    "standard_type" "text" DEFAULT 'test_method'::"text",
    "url" "text",
    "revision" "text",
    "is_active" boolean DEFAULT true,
    "created_at" timestamp with time zone DEFAULT "now"(),
    "updated_at" timestamp with time zone DEFAULT "now"(),
    CONSTRAINT "standards_standard_type_check" CHECK (("standard_type" = ANY (ARRAY['test_method'::"text", 'certification'::"text", 'accreditation'::"text", 'compliance'::"text"])))
);


ALTER TABLE "public"."standards" OWNER TO "postgres";


COMMENT ON TABLE "public"."standards" IS 'Testing standards, certifications, and test methods across all industries';



CREATE TABLE IF NOT EXISTS "public"."subscription_invoices" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "user_id" "uuid" NOT NULL,
    "tier" "text" NOT NULL,
    "amount" numeric(10,2) NOT NULL,
    "currency" "text" DEFAULT 'USD'::"text" NOT NULL,
    "status" "text" DEFAULT 'pending'::"text" NOT NULL,
    "invoice_date" "date" DEFAULT CURRENT_DATE NOT NULL,
    "due_date" "date" NOT NULL,
    "paid_date" "date",
    "payment_method" "text",
    "payment_reference" "text",
    "notes" "text",
    "admin_notes" "text",
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "updated_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    CONSTRAINT "subscription_invoices_amount_check" CHECK (("amount" > (0)::numeric)),
    CONSTRAINT "subscription_invoices_payment_method_check" CHECK (("payment_method" = ANY (ARRAY['paypal'::"text", 'eft'::"text", 'bank_transfer'::"text", 'stripe'::"text"]))),
    CONSTRAINT "subscription_invoices_status_check" CHECK (("status" = ANY (ARRAY['pending'::"text", 'paid'::"text", 'overdue'::"text", 'cancelled'::"text", 'refunded'::"text"]))),
    CONSTRAINT "subscription_invoices_tier_check" CHECK (("tier" = ANY (ARRAY['professional'::"text", 'premium'::"text", 'enterprise'::"text", 'verification'::"text"])))
);


ALTER TABLE "public"."subscription_invoices" OWNER TO "postgres";


COMMENT ON TABLE "public"."subscription_invoices" IS 'Manual invoice tracking for subscriptions (before payment automation)';



COMMENT ON COLUMN "public"."subscription_invoices"."tier" IS 'Subscription tier or one-time purchase (e.g., verification)';



CREATE TABLE IF NOT EXISTS "public"."user_profiles" (
    "id" "uuid" NOT NULL,
    "subscription_tier" "text" DEFAULT 'free'::"text" NOT NULL,
    "subscription_status" "text" DEFAULT 'active'::"text" NOT NULL,
    "subscription_start_date" timestamp with time zone,
    "subscription_end_date" timestamp with time zone,
    "payment_method" "text" DEFAULT 'manual'::"text",
    "company_name" "text",
    "billing_email" "text",
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "updated_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "role" "text" DEFAULT 'user'::"text",
    "paypal_subscription_id" "text",
    "last_payment_date" timestamp with time zone,
    CONSTRAINT "user_profiles_payment_method_check" CHECK (("payment_method" = ANY (ARRAY['manual'::"text", 'paypal'::"text", 'stripe'::"text", 'eft'::"text", 'bank_transfer'::"text"]))),
    CONSTRAINT "user_profiles_role_check" CHECK (("role" = ANY (ARRAY['user'::"text", 'admin'::"text"]))),
    CONSTRAINT "user_profiles_subscription_status_check" CHECK (("subscription_status" = ANY (ARRAY['active'::"text", 'cancelled'::"text", 'past_due'::"text", 'trialing'::"text"]))),
    CONSTRAINT "user_profiles_subscription_tier_check" CHECK (("subscription_tier" = ANY (ARRAY['free'::"text", 'basic'::"text", 'professional'::"text", 'premium'::"text", 'enterprise'::"text"])))
);


ALTER TABLE "public"."user_profiles" OWNER TO "postgres";


COMMENT ON TABLE "public"."user_profiles" IS 'Extended user profile with subscription tier information';



COMMENT ON COLUMN "public"."user_profiles"."subscription_tier" IS 'Current subscription tier: free, basic, professional, premium, enterprise';



COMMENT ON COLUMN "public"."user_profiles"."payment_method" IS 'Payment method on file (manual for initial PayPal/EFT invoicing)';



CREATE TABLE IF NOT EXISTS "public"."waitlist" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "email" "text" NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"(),
    "source" "text" DEFAULT 'website'::"text",
    "status" "text" DEFAULT 'pending'::"text",
    "notes" "text"
);


ALTER TABLE "public"."waitlist" OWNER TO "postgres";


ALTER TABLE ONLY "public"."categories"
    ADD CONSTRAINT "categories_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."categories"
    ADD CONSTRAINT "categories_slug_key" UNIQUE ("slug");



ALTER TABLE ONLY "public"."claims"
    ADD CONSTRAINT "claims_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."clicks"
    ADD CONSTRAINT "clicks_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."custom_fields"
    ADD CONSTRAINT "custom_fields_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."listing_capabilities"
    ADD CONSTRAINT "listing_capabilities_listing_id_standard_id_key" UNIQUE ("listing_id", "standard_id");



ALTER TABLE ONLY "public"."listing_capabilities"
    ADD CONSTRAINT "listing_capabilities_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."listing_categories"
    ADD CONSTRAINT "listing_categories_listing_id_category_id_key" UNIQUE ("listing_id", "category_id");



ALTER TABLE ONLY "public"."listing_categories"
    ADD CONSTRAINT "listing_categories_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."listing_custom_fields"
    ADD CONSTRAINT "listing_custom_fields_listing_id_custom_field_id_key" UNIQUE ("listing_id", "custom_field_id");



ALTER TABLE ONLY "public"."listing_custom_fields"
    ADD CONSTRAINT "listing_custom_fields_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."listing_images"
    ADD CONSTRAINT "listing_images_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."listing_owners"
    ADD CONSTRAINT "listing_owners_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."listing_owners"
    ADD CONSTRAINT "listing_owners_user_id_listing_id_key" UNIQUE ("user_id", "listing_id");



ALTER TABLE ONLY "public"."listing_ownership"
    ADD CONSTRAINT "listing_ownership_listing_id_user_id_key" UNIQUE ("listing_id", "user_id");



ALTER TABLE ONLY "public"."listing_ownership"
    ADD CONSTRAINT "listing_ownership_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."listings"
    ADD CONSTRAINT "listings_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."listings"
    ADD CONSTRAINT "listings_slug_key" UNIQUE ("slug");



ALTER TABLE ONLY "public"."locations"
    ADD CONSTRAINT "locations_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."locations"
    ADD CONSTRAINT "locations_slug_key" UNIQUE ("slug");



ALTER TABLE ONLY "public"."payment_history"
    ADD CONSTRAINT "payment_history_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."payments"
    ADD CONSTRAINT "payments_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."pending_research"
    ADD CONSTRAINT "pending_research_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."schema_migrations"
    ADD CONSTRAINT "schema_migrations_pkey" PRIMARY KEY ("version");



ALTER TABLE ONLY "public"."search_logs"
    ADD CONSTRAINT "search_logs_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."standards"
    ADD CONSTRAINT "standards_code_key" UNIQUE ("code");



ALTER TABLE ONLY "public"."standards"
    ADD CONSTRAINT "standards_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."subscription_invoices"
    ADD CONSTRAINT "subscription_invoices_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."user_profiles"
    ADD CONSTRAINT "user_profiles_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."waitlist"
    ADD CONSTRAINT "waitlist_email_key" UNIQUE ("email");



ALTER TABLE ONLY "public"."waitlist"
    ADD CONSTRAINT "waitlist_pkey" PRIMARY KEY ("id");



CREATE INDEX "idx_capabilities_listing" ON "public"."listing_capabilities" USING "btree" ("listing_id");



CREATE INDEX "idx_capabilities_specs" ON "public"."listing_capabilities" USING "gin" ("specifications");



CREATE INDEX "idx_capabilities_standard" ON "public"."listing_capabilities" USING "btree" ("standard_id");



CREATE INDEX "idx_categories_parent" ON "public"."categories" USING "btree" ("parent_id");



CREATE INDEX "idx_categories_slug" ON "public"."categories" USING "btree" ("slug");



CREATE INDEX "idx_claims_email" ON "public"."claims" USING "btree" ("business_email");



CREATE INDEX "idx_claims_status" ON "public"."claims" USING "btree" ("status");



CREATE INDEX "idx_clicks_created" ON "public"."clicks" USING "btree" ("created_at" DESC);



CREATE INDEX "idx_clicks_listing" ON "public"."clicks" USING "btree" ("listing_id");



CREATE INDEX "idx_custom_fields_category" ON "public"."custom_fields" USING "btree" ("category_id");



CREATE INDEX "idx_listing_custom_fields_field" ON "public"."listing_custom_fields" USING "btree" ("custom_field_id");



CREATE INDEX "idx_listing_custom_fields_listing" ON "public"."listing_custom_fields" USING "btree" ("listing_id");



CREATE INDEX "idx_listing_images_listing" ON "public"."listing_images" USING "btree" ("listing_id");



CREATE INDEX "idx_listing_owners_listing_id" ON "public"."listing_owners" USING "btree" ("listing_id");



CREATE INDEX "idx_listing_owners_status" ON "public"."listing_owners" USING "btree" ("status");



CREATE INDEX "idx_listing_owners_user_id" ON "public"."listing_owners" USING "btree" ("user_id");



CREATE INDEX "idx_listing_ownership_listing_id" ON "public"."listing_ownership" USING "btree" ("listing_id");



CREATE INDEX "idx_listing_ownership_user_id" ON "public"."listing_ownership" USING "btree" ("user_id");



CREATE INDEX "idx_listings_category" ON "public"."listings" USING "btree" ("category_id");



CREATE INDEX "idx_listings_claimed" ON "public"."listings" USING "btree" ("claimed");



CREATE INDEX "idx_listings_featured" ON "public"."listings" USING "btree" ("is_featured", "featured_until") WHERE ("is_featured" = true);



CREATE INDEX "idx_listings_location" ON "public"."listings" USING "btree" ("location_id");



CREATE INDEX "idx_listings_priority_rank" ON "public"."listings" USING "btree" ("priority_rank" DESC);



CREATE INDEX "idx_listings_region" ON "public"."listings" USING "btree" ("region");



CREATE INDEX "idx_listings_script_location" ON "public"."listings" USING "btree" ("script_location");



CREATE INDEX "idx_listings_slug" ON "public"."listings" USING "btree" ("slug");



CREATE INDEX "idx_listings_source_script" ON "public"."listings" USING "btree" ("source_script");



CREATE INDEX "idx_listings_status" ON "public"."listings" USING "btree" ("status") WHERE ("status" = 'active'::"text");



CREATE INDEX "idx_listings_website_domain" ON "public"."listings" USING "btree" ("website_domain");



CREATE INDEX "idx_locations_level" ON "public"."locations" USING "btree" ("level");



CREATE INDEX "idx_locations_parent" ON "public"."locations" USING "btree" ("parent_id");



CREATE INDEX "idx_locations_slug" ON "public"."locations" USING "btree" ("slug");



CREATE INDEX "idx_payment_history_created_at" ON "public"."payment_history" USING "btree" ("created_at" DESC);



CREATE INDEX "idx_payment_history_user_id" ON "public"."payment_history" USING "btree" ("user_id");



CREATE INDEX "idx_payments_listing" ON "public"."payments" USING "btree" ("listing_id");



CREATE INDEX "idx_payments_owner" ON "public"."payments" USING "btree" ("owner_id");



CREATE INDEX "idx_payments_status" ON "public"."payments" USING "btree" ("status");



CREATE INDEX "idx_pending_research_business_name" ON "public"."pending_research" USING "btree" ("business_name");



CREATE INDEX "idx_pending_research_status" ON "public"."pending_research" USING "btree" ("status");



CREATE INDEX "idx_standards_active" ON "public"."standards" USING "btree" ("is_active") WHERE ("is_active" = true);



CREATE INDEX "idx_standards_category" ON "public"."standards" USING "btree" ("category_id");



CREATE INDEX "idx_standards_code" ON "public"."standards" USING "btree" ("code");



CREATE INDEX "idx_standards_issuing_body" ON "public"."standards" USING "btree" ("issuing_body");



CREATE INDEX "idx_subscription_invoices_due_date" ON "public"."subscription_invoices" USING "btree" ("due_date");



CREATE INDEX "idx_subscription_invoices_status" ON "public"."subscription_invoices" USING "btree" ("status");



CREATE INDEX "idx_subscription_invoices_user_id" ON "public"."subscription_invoices" USING "btree" ("user_id");



CREATE INDEX "idx_user_profiles_subscription_tier" ON "public"."user_profiles" USING "btree" ("subscription_tier");



CREATE INDEX "idx_waitlist_created_at" ON "public"."waitlist" USING "btree" ("created_at" DESC);



CREATE INDEX "idx_waitlist_email" ON "public"."waitlist" USING "btree" ("email");



CREATE OR REPLACE TRIGGER "trigger_update_website_domain" BEFORE INSERT OR UPDATE ON "public"."listings" FOR EACH ROW EXECUTE FUNCTION "public"."update_website_domain"();



CREATE OR REPLACE TRIGGER "update_subscription_invoices_updated_at" BEFORE UPDATE ON "public"."subscription_invoices" FOR EACH ROW EXECUTE FUNCTION "public"."update_updated_at_column"();



CREATE OR REPLACE TRIGGER "update_user_profiles_updated_at" BEFORE UPDATE ON "public"."user_profiles" FOR EACH ROW EXECUTE FUNCTION "public"."update_updated_at_column"();



ALTER TABLE ONLY "public"."categories"
    ADD CONSTRAINT "categories_parent_id_fkey" FOREIGN KEY ("parent_id") REFERENCES "public"."categories"("id") ON DELETE SET NULL;



ALTER TABLE ONLY "public"."clicks"
    ADD CONSTRAINT "clicks_listing_id_fkey" FOREIGN KEY ("listing_id") REFERENCES "public"."listings"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."custom_fields"
    ADD CONSTRAINT "custom_fields_category_id_fkey" FOREIGN KEY ("category_id") REFERENCES "public"."categories"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."listing_capabilities"
    ADD CONSTRAINT "listing_capabilities_listing_id_fkey" FOREIGN KEY ("listing_id") REFERENCES "public"."listings"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."listing_capabilities"
    ADD CONSTRAINT "listing_capabilities_standard_id_fkey" FOREIGN KEY ("standard_id") REFERENCES "public"."standards"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."listing_capabilities"
    ADD CONSTRAINT "listing_capabilities_verified_by_fkey" FOREIGN KEY ("verified_by") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."listing_categories"
    ADD CONSTRAINT "listing_categories_category_id_fkey" FOREIGN KEY ("category_id") REFERENCES "public"."categories"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."listing_categories"
    ADD CONSTRAINT "listing_categories_listing_id_fkey" FOREIGN KEY ("listing_id") REFERENCES "public"."listings"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."listing_custom_fields"
    ADD CONSTRAINT "listing_custom_fields_custom_field_id_fkey" FOREIGN KEY ("custom_field_id") REFERENCES "public"."custom_fields"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."listing_custom_fields"
    ADD CONSTRAINT "listing_custom_fields_listing_id_fkey" FOREIGN KEY ("listing_id") REFERENCES "public"."listings"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."listing_images"
    ADD CONSTRAINT "listing_images_listing_id_fkey" FOREIGN KEY ("listing_id") REFERENCES "public"."listings"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."listing_owners"
    ADD CONSTRAINT "listing_owners_listing_id_fkey" FOREIGN KEY ("listing_id") REFERENCES "public"."listings"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."listing_owners"
    ADD CONSTRAINT "listing_owners_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."listing_ownership"
    ADD CONSTRAINT "listing_ownership_listing_id_fkey" FOREIGN KEY ("listing_id") REFERENCES "public"."listings"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."listing_ownership"
    ADD CONSTRAINT "listing_ownership_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."listing_ownership"
    ADD CONSTRAINT "listing_ownership_verified_by_fkey" FOREIGN KEY ("verified_by") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."listings"
    ADD CONSTRAINT "listings_category_id_fkey" FOREIGN KEY ("category_id") REFERENCES "public"."categories"("id");



ALTER TABLE ONLY "public"."listings"
    ADD CONSTRAINT "listings_location_id_fkey" FOREIGN KEY ("location_id") REFERENCES "public"."locations"("id");



ALTER TABLE ONLY "public"."listings"
    ADD CONSTRAINT "listings_owner_id_fkey" FOREIGN KEY ("owner_id") REFERENCES "auth"."users"("id") ON DELETE SET NULL;



ALTER TABLE ONLY "public"."listings"
    ADD CONSTRAINT "listings_parent_listing_id_fkey" FOREIGN KEY ("parent_listing_id") REFERENCES "public"."listings"("id") ON DELETE SET NULL;



ALTER TABLE ONLY "public"."locations"
    ADD CONSTRAINT "locations_parent_id_fkey" FOREIGN KEY ("parent_id") REFERENCES "public"."locations"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."payment_history"
    ADD CONSTRAINT "payment_history_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."payments"
    ADD CONSTRAINT "payments_listing_id_fkey" FOREIGN KEY ("listing_id") REFERENCES "public"."listings"("id") ON DELETE SET NULL;



ALTER TABLE ONLY "public"."payments"
    ADD CONSTRAINT "payments_owner_id_fkey" FOREIGN KEY ("owner_id") REFERENCES "auth"."users"("id") ON DELETE SET NULL;



ALTER TABLE ONLY "public"."payments"
    ADD CONSTRAINT "payments_verified_by_fkey" FOREIGN KEY ("verified_by") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."standards"
    ADD CONSTRAINT "standards_category_id_fkey" FOREIGN KEY ("category_id") REFERENCES "public"."categories"("id");



ALTER TABLE ONLY "public"."subscription_invoices"
    ADD CONSTRAINT "subscription_invoices_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."user_profiles"
    ADD CONSTRAINT "user_profiles_id_fkey" FOREIGN KEY ("id") REFERENCES "auth"."users"("id") ON DELETE CASCADE;



CREATE POLICY "Admins can manage all capabilities" ON "public"."listing_capabilities" USING (("auth"."role"() = 'authenticated'::"text"));



CREATE POLICY "Admins can manage standards" ON "public"."standards" USING (("auth"."role"() = 'authenticated'::"text"));



CREATE POLICY "Admins can update ownership status" ON "public"."listing_owners" FOR UPDATE USING ((EXISTS ( SELECT 1
   FROM "public"."user_profiles"
  WHERE (("user_profiles"."id" = ( SELECT "auth"."uid"() AS "uid")) AND ("listing_owners"."role" = 'admin'::"text")))));



CREATE POLICY "Allow anonymous claim submissions" ON "public"."claims" FOR INSERT TO "anon" WITH CHECK (true);



CREATE POLICY "Allow authenticated submissions to pending listings" ON "public"."listings" FOR INSERT TO "authenticated" WITH CHECK ((("status" = 'pending'::"text") AND ("verified" = false) AND ("claimed" = false)));



CREATE POLICY "Allow public read access to active listings" ON "public"."listings" FOR SELECT TO "anon" USING (("status" = 'active'::"text"));



CREATE POLICY "Allow public read access to all categories" ON "public"."categories" FOR SELECT TO "anon" USING (true);



CREATE POLICY "Allow public read access to categories" ON "public"."categories" FOR SELECT TO "anon" USING (true);



CREATE POLICY "Allow public read access to locations" ON "public"."locations" FOR SELECT TO "anon" USING (true);



CREATE POLICY "Allow public submissions to pending listings" ON "public"."listings" FOR INSERT TO "anon" WITH CHECK ((("status" = 'pending'::"text") AND ("verified" = false) AND ("claimed" = false)));



CREATE POLICY "Anyone can log clicks" ON "public"."clicks" FOR INSERT TO "anon" WITH CHECK (true);



CREATE POLICY "Anyone can submit to waitlist" ON "public"."waitlist" FOR INSERT WITH CHECK (true);



CREATE POLICY "Authenticated users can read waitlist" ON "public"."waitlist" FOR SELECT TO "authenticated" USING (true);



CREATE POLICY "Authenticated users can view active listings" ON "public"."listings" FOR SELECT TO "authenticated" USING (("status" = 'active'::"text"));



CREATE POLICY "Authenticated users can view all clicks" ON "public"."clicks" FOR SELECT TO "authenticated" USING (true);



CREATE POLICY "Capabilities are publicly readable" ON "public"."listing_capabilities" FOR SELECT USING (true);



CREATE POLICY "Enable all for authenticated users" ON "public"."pending_research" USING (true);



CREATE POLICY "Listing owners can manage their capabilities" ON "public"."listing_capabilities" USING (("listing_id" IN ( SELECT "listings"."id"
   FROM "public"."listings"
  WHERE ("listings"."owner_id" = "auth"."uid"()))));



CREATE POLICY "Listing owners can manage their capabilities" ON "public"."listing_owners" USING (("listing_id" IN ( SELECT "listings"."id"
   FROM "public"."listings"
  WHERE ("listings"."owner_id" = ( SELECT "auth"."uid"() AS "uid")))));



CREATE POLICY "Listing owners can update their listings" ON "public"."listings" FOR UPDATE TO "authenticated" USING (("id" IN ( SELECT "listing_ownership"."listing_id"
   FROM "public"."listing_ownership"
  WHERE (("listing_ownership"."user_id" = ( SELECT "auth"."uid"() AS "uid")) AND ("listing_ownership"."verified_owner" = true)))));



CREATE POLICY "Public read" ON "public"."listing_categories" FOR SELECT USING (true);



CREATE POLICY "Service role" ON "public"."listing_categories" USING (("auth"."role"() = 'service_role'::"text"));



CREATE POLICY "Service role can insert payments" ON "public"."payment_history" FOR INSERT WITH CHECK (true);



CREATE POLICY "Service role can manage waitlist" ON "public"."waitlist" TO "service_role" USING (true) WITH CHECK (true);



CREATE POLICY "Standards are publicly readable" ON "public"."standards" FOR SELECT USING (true);



CREATE POLICY "Users can claim listings" ON "public"."claims" FOR INSERT WITH CHECK (("business_email" = ( SELECT ("auth"."jwt"() ->> 'email'::"text"))));



CREATE POLICY "Users can claim listings" ON "public"."listing_owners" FOR INSERT WITH CHECK (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can claim listings" ON "public"."listing_ownership" FOR INSERT TO "authenticated" WITH CHECK (("user_id" = "auth"."uid"()));



CREATE POLICY "Users can claim listings (authenticated)" ON "public"."claims" FOR INSERT TO "authenticated" WITH CHECK (("business_email" = ( SELECT ("auth"."jwt"() ->> 'email'::"text"))));



CREATE POLICY "Users can insert own profile" ON "public"."user_profiles" FOR INSERT TO "authenticated" WITH CHECK (("id" = ( SELECT "auth"."uid"() AS "uid")));



CREATE POLICY "Users can update own pending claims" ON "public"."claims" FOR UPDATE USING ((("business_email" = ( SELECT ("auth"."jwt"() ->> 'email'::"text"))) AND ("status" = 'pending'::"text")));



CREATE POLICY "Users can update own pending claims" ON "public"."listing_owners" FOR UPDATE USING ((("auth"."uid"() = "user_id") AND ("status" = 'pending'::"text")));



CREATE POLICY "Users can update own profile" ON "public"."user_profiles" FOR UPDATE TO "authenticated" USING (("id" = ( SELECT "auth"."uid"() AS "uid"))) WITH CHECK (("id" = ( SELECT "auth"."uid"() AS "uid")));



CREATE POLICY "Users can view own invoices" ON "public"."subscription_invoices" FOR SELECT TO "authenticated" USING (("user_id" = ( SELECT "auth"."uid"() AS "uid")));



CREATE POLICY "Users can view own listing ownerships" ON "public"."listing_ownership" FOR SELECT TO "authenticated" USING (("user_id" = ( SELECT "auth"."uid"() AS "uid")));



CREATE POLICY "Users can view own ownership" ON "public"."listing_owners" FOR SELECT USING (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can view own ownership" ON "public"."listing_ownership" FOR SELECT USING ((( SELECT "auth"."uid"() AS "uid") = "user_id"));



CREATE POLICY "Users can view own payment history" ON "public"."payment_history" FOR SELECT USING (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can view own profile" ON "public"."user_profiles" FOR SELECT TO "authenticated" USING (("id" = ( SELECT "auth"."uid"() AS "uid")));



CREATE POLICY "Users can view their own claims" ON "public"."claims" FOR SELECT TO "authenticated" USING (("business_email" = ( SELECT ("auth"."jwt"() ->> 'email'::"text"))));



ALTER TABLE "public"."categories" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."claims" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."clicks" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."custom_fields" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."listing_capabilities" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."listing_categories" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."listing_custom_fields" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."listing_images" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."listing_owners" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."listing_ownership" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."listings" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."locations" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."payment_history" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."payments" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."pending_research" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."search_logs" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."standards" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."subscription_invoices" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."user_profiles" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."waitlist" ENABLE ROW LEVEL SECURITY;




ALTER PUBLICATION "supabase_realtime" OWNER TO "postgres";


GRANT USAGE ON SCHEMA "public" TO "postgres";
GRANT USAGE ON SCHEMA "public" TO "anon";
GRANT USAGE ON SCHEMA "public" TO "authenticated";
GRANT USAGE ON SCHEMA "public" TO "service_role";




































































































































































































































































































































GRANT ALL ON FUNCTION "public"."can_auto_claim"("user_email" "text", "listing_website" "text") TO "anon";
GRANT ALL ON FUNCTION "public"."can_auto_claim"("user_email" "text", "listing_website" "text") TO "authenticated";
GRANT ALL ON FUNCTION "public"."can_auto_claim"("user_email" "text", "listing_website" "text") TO "service_role";



GRANT ALL ON FUNCTION "public"."can_view_contact_info"("user_uuid" "uuid") TO "anon";
GRANT ALL ON FUNCTION "public"."can_view_contact_info"("user_uuid" "uuid") TO "authenticated";
GRANT ALL ON FUNCTION "public"."can_view_contact_info"("user_uuid" "uuid") TO "service_role";



GRANT ALL ON FUNCTION "public"."extract_domain"("url" "text") TO "anon";
GRANT ALL ON FUNCTION "public"."extract_domain"("url" "text") TO "authenticated";
GRANT ALL ON FUNCTION "public"."extract_domain"("url" "text") TO "service_role";



GRANT ALL ON FUNCTION "public"."get_click_stats"("days_back" integer) TO "anon";
GRANT ALL ON FUNCTION "public"."get_click_stats"("days_back" integer) TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_click_stats"("days_back" integer) TO "service_role";



GRANT ALL ON FUNCTION "public"."get_top_clicked_listings"("limit_count" integer) TO "anon";
GRANT ALL ON FUNCTION "public"."get_top_clicked_listings"("limit_count" integer) TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_top_clicked_listings"("limit_count" integer) TO "service_role";



GRANT ALL ON FUNCTION "public"."get_user_tier"("user_uuid" "uuid") TO "anon";
GRANT ALL ON FUNCTION "public"."get_user_tier"("user_uuid" "uuid") TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_user_tier"("user_uuid" "uuid") TO "service_role";



GRANT ALL ON FUNCTION "public"."handle_new_user"() TO "anon";
GRANT ALL ON FUNCTION "public"."handle_new_user"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."handle_new_user"() TO "service_role";



GRANT ALL ON FUNCTION "public"."make_user_admin"("user_email" "text") TO "anon";
GRANT ALL ON FUNCTION "public"."make_user_admin"("user_email" "text") TO "authenticated";
GRANT ALL ON FUNCTION "public"."make_user_admin"("user_email" "text") TO "service_role";



GRANT ALL ON FUNCTION "public"."search_by_standard"("p_standard_code" "text", "p_category_id" "uuid", "p_min_specs" "jsonb") TO "anon";
GRANT ALL ON FUNCTION "public"."search_by_standard"("p_standard_code" "text", "p_category_id" "uuid", "p_min_specs" "jsonb") TO "authenticated";
GRANT ALL ON FUNCTION "public"."search_by_standard"("p_standard_code" "text", "p_category_id" "uuid", "p_min_specs" "jsonb") TO "service_role";



GRANT ALL ON FUNCTION "public"."update_updated_at_column"() TO "anon";
GRANT ALL ON FUNCTION "public"."update_updated_at_column"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."update_updated_at_column"() TO "service_role";



GRANT ALL ON FUNCTION "public"."update_website_domain"() TO "anon";
GRANT ALL ON FUNCTION "public"."update_website_domain"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."update_website_domain"() TO "service_role";



GRANT ALL ON FUNCTION "public"."user_owns_listing"("user_uuid" "uuid", "listing_uuid" "uuid") TO "anon";
GRANT ALL ON FUNCTION "public"."user_owns_listing"("user_uuid" "uuid", "listing_uuid" "uuid") TO "authenticated";
GRANT ALL ON FUNCTION "public"."user_owns_listing"("user_uuid" "uuid", "listing_uuid" "uuid") TO "service_role";



























GRANT ALL ON TABLE "public"."categories" TO "anon";
GRANT ALL ON TABLE "public"."categories" TO "authenticated";
GRANT ALL ON TABLE "public"."categories" TO "service_role";



GRANT ALL ON TABLE "public"."claims" TO "anon";
GRANT ALL ON TABLE "public"."claims" TO "authenticated";
GRANT ALL ON TABLE "public"."claims" TO "service_role";



GRANT ALL ON TABLE "public"."clicks" TO "anon";
GRANT ALL ON TABLE "public"."clicks" TO "authenticated";
GRANT ALL ON TABLE "public"."clicks" TO "service_role";



GRANT ALL ON TABLE "public"."custom_fields" TO "anon";
GRANT ALL ON TABLE "public"."custom_fields" TO "authenticated";
GRANT ALL ON TABLE "public"."custom_fields" TO "service_role";



GRANT ALL ON TABLE "public"."listing_capabilities" TO "anon";
GRANT ALL ON TABLE "public"."listing_capabilities" TO "authenticated";
GRANT ALL ON TABLE "public"."listing_capabilities" TO "service_role";



GRANT ALL ON TABLE "public"."listing_categories" TO "anon";
GRANT ALL ON TABLE "public"."listing_categories" TO "authenticated";
GRANT ALL ON TABLE "public"."listing_categories" TO "service_role";



GRANT ALL ON TABLE "public"."listing_custom_fields" TO "anon";
GRANT ALL ON TABLE "public"."listing_custom_fields" TO "authenticated";
GRANT ALL ON TABLE "public"."listing_custom_fields" TO "service_role";



GRANT ALL ON TABLE "public"."listing_images" TO "anon";
GRANT ALL ON TABLE "public"."listing_images" TO "authenticated";
GRANT ALL ON TABLE "public"."listing_images" TO "service_role";



GRANT ALL ON TABLE "public"."listing_owners" TO "anon";
GRANT ALL ON TABLE "public"."listing_owners" TO "authenticated";
GRANT ALL ON TABLE "public"."listing_owners" TO "service_role";



GRANT ALL ON TABLE "public"."listing_ownership" TO "anon";
GRANT ALL ON TABLE "public"."listing_ownership" TO "authenticated";
GRANT ALL ON TABLE "public"."listing_ownership" TO "service_role";



GRANT ALL ON TABLE "public"."listings" TO "anon";
GRANT ALL ON TABLE "public"."listings" TO "authenticated";
GRANT ALL ON TABLE "public"."listings" TO "service_role";



GRANT ALL ON TABLE "public"."locations" TO "anon";
GRANT ALL ON TABLE "public"."locations" TO "authenticated";
GRANT ALL ON TABLE "public"."locations" TO "service_role";



GRANT ALL ON TABLE "public"."payment_history" TO "anon";
GRANT ALL ON TABLE "public"."payment_history" TO "authenticated";
GRANT ALL ON TABLE "public"."payment_history" TO "service_role";



GRANT ALL ON TABLE "public"."payments" TO "anon";
GRANT ALL ON TABLE "public"."payments" TO "authenticated";
GRANT ALL ON TABLE "public"."payments" TO "service_role";



GRANT ALL ON TABLE "public"."pending_research" TO "anon";
GRANT ALL ON TABLE "public"."pending_research" TO "authenticated";
GRANT ALL ON TABLE "public"."pending_research" TO "service_role";



GRANT ALL ON TABLE "public"."potential_dead_links" TO "anon";
GRANT ALL ON TABLE "public"."potential_dead_links" TO "authenticated";
GRANT ALL ON TABLE "public"."potential_dead_links" TO "service_role";



GRANT ALL ON TABLE "public"."schema_migrations" TO "anon";
GRANT ALL ON TABLE "public"."schema_migrations" TO "authenticated";
GRANT ALL ON TABLE "public"."schema_migrations" TO "service_role";



GRANT ALL ON TABLE "public"."search_logs" TO "anon";
GRANT ALL ON TABLE "public"."search_logs" TO "authenticated";
GRANT ALL ON TABLE "public"."search_logs" TO "service_role";



GRANT ALL ON TABLE "public"."standards" TO "anon";
GRANT ALL ON TABLE "public"."standards" TO "authenticated";
GRANT ALL ON TABLE "public"."standards" TO "service_role";



GRANT ALL ON TABLE "public"."subscription_invoices" TO "anon";
GRANT ALL ON TABLE "public"."subscription_invoices" TO "authenticated";
GRANT ALL ON TABLE "public"."subscription_invoices" TO "service_role";



GRANT ALL ON TABLE "public"."user_profiles" TO "anon";
GRANT ALL ON TABLE "public"."user_profiles" TO "authenticated";
GRANT ALL ON TABLE "public"."user_profiles" TO "service_role";



GRANT ALL ON TABLE "public"."waitlist" TO "anon";
GRANT ALL ON TABLE "public"."waitlist" TO "authenticated";
GRANT ALL ON TABLE "public"."waitlist" TO "service_role";









ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "service_role";































drop extension if exists "pg_net";

drop trigger if exists "trigger_update_website_domain" on "public"."listings";

drop trigger if exists "update_subscription_invoices_updated_at" on "public"."subscription_invoices";

drop trigger if exists "update_user_profiles_updated_at" on "public"."user_profiles";

drop policy "Listing owners can manage their capabilities" on "public"."listing_capabilities";

drop policy "Admins can update ownership status" on "public"."listing_owners";

drop policy "Listing owners can manage their capabilities" on "public"."listing_owners";

drop policy "Listing owners can update their listings" on "public"."listings";

alter table "public"."categories" drop constraint "categories_parent_id_fkey";

alter table "public"."clicks" drop constraint "clicks_listing_id_fkey";

alter table "public"."custom_fields" drop constraint "custom_fields_category_id_fkey";

alter table "public"."listing_capabilities" drop constraint "listing_capabilities_listing_id_fkey";

alter table "public"."listing_capabilities" drop constraint "listing_capabilities_standard_id_fkey";

alter table "public"."listing_categories" drop constraint "listing_categories_category_id_fkey";

alter table "public"."listing_categories" drop constraint "listing_categories_listing_id_fkey";

alter table "public"."listing_custom_fields" drop constraint "listing_custom_fields_custom_field_id_fkey";

alter table "public"."listing_custom_fields" drop constraint "listing_custom_fields_listing_id_fkey";

alter table "public"."listing_images" drop constraint "listing_images_listing_id_fkey";

alter table "public"."listing_owners" drop constraint "listing_owners_listing_id_fkey";

alter table "public"."listing_ownership" drop constraint "listing_ownership_listing_id_fkey";

alter table "public"."listings" drop constraint "listings_category_id_fkey";

alter table "public"."listings" drop constraint "listings_location_id_fkey";

alter table "public"."listings" drop constraint "listings_parent_listing_id_fkey";

alter table "public"."locations" drop constraint "locations_parent_id_fkey";

alter table "public"."payments" drop constraint "payments_listing_id_fkey";

alter table "public"."standards" drop constraint "standards_category_id_fkey";

alter table "public"."categories" alter column "id" set default extensions.uuid_generate_v4();

alter table "public"."custom_fields" alter column "id" set default extensions.uuid_generate_v4();

alter table "public"."listing_capabilities" alter column "id" set default extensions.uuid_generate_v4();

alter table "public"."listing_custom_fields" alter column "id" set default extensions.uuid_generate_v4();

alter table "public"."listing_images" alter column "id" set default extensions.uuid_generate_v4();

alter table "public"."listing_owners" alter column "id" set default extensions.uuid_generate_v4();

alter table "public"."listings" alter column "id" set default extensions.uuid_generate_v4();

alter table "public"."locations" alter column "id" set default extensions.uuid_generate_v4();

alter table "public"."payments" alter column "id" set default extensions.uuid_generate_v4();

alter table "public"."search_logs" alter column "id" set default extensions.uuid_generate_v4();

alter table "public"."standards" alter column "id" set default extensions.uuid_generate_v4();

alter table "public"."categories" add constraint "categories_parent_id_fkey" FOREIGN KEY (parent_id) REFERENCES public.categories(id) ON DELETE SET NULL not valid;

alter table "public"."categories" validate constraint "categories_parent_id_fkey";

alter table "public"."clicks" add constraint "clicks_listing_id_fkey" FOREIGN KEY (listing_id) REFERENCES public.listings(id) ON DELETE CASCADE not valid;

alter table "public"."clicks" validate constraint "clicks_listing_id_fkey";

alter table "public"."custom_fields" add constraint "custom_fields_category_id_fkey" FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE CASCADE not valid;

alter table "public"."custom_fields" validate constraint "custom_fields_category_id_fkey";

alter table "public"."listing_capabilities" add constraint "listing_capabilities_listing_id_fkey" FOREIGN KEY (listing_id) REFERENCES public.listings(id) ON DELETE CASCADE not valid;

alter table "public"."listing_capabilities" validate constraint "listing_capabilities_listing_id_fkey";

alter table "public"."listing_capabilities" add constraint "listing_capabilities_standard_id_fkey" FOREIGN KEY (standard_id) REFERENCES public.standards(id) ON DELETE CASCADE not valid;

alter table "public"."listing_capabilities" validate constraint "listing_capabilities_standard_id_fkey";

alter table "public"."listing_categories" add constraint "listing_categories_category_id_fkey" FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE CASCADE not valid;

alter table "public"."listing_categories" validate constraint "listing_categories_category_id_fkey";

alter table "public"."listing_categories" add constraint "listing_categories_listing_id_fkey" FOREIGN KEY (listing_id) REFERENCES public.listings(id) ON DELETE CASCADE not valid;

alter table "public"."listing_categories" validate constraint "listing_categories_listing_id_fkey";

alter table "public"."listing_custom_fields" add constraint "listing_custom_fields_custom_field_id_fkey" FOREIGN KEY (custom_field_id) REFERENCES public.custom_fields(id) ON DELETE CASCADE not valid;

alter table "public"."listing_custom_fields" validate constraint "listing_custom_fields_custom_field_id_fkey";

alter table "public"."listing_custom_fields" add constraint "listing_custom_fields_listing_id_fkey" FOREIGN KEY (listing_id) REFERENCES public.listings(id) ON DELETE CASCADE not valid;

alter table "public"."listing_custom_fields" validate constraint "listing_custom_fields_listing_id_fkey";

alter table "public"."listing_images" add constraint "listing_images_listing_id_fkey" FOREIGN KEY (listing_id) REFERENCES public.listings(id) ON DELETE CASCADE not valid;

alter table "public"."listing_images" validate constraint "listing_images_listing_id_fkey";

alter table "public"."listing_owners" add constraint "listing_owners_listing_id_fkey" FOREIGN KEY (listing_id) REFERENCES public.listings(id) ON DELETE CASCADE not valid;

alter table "public"."listing_owners" validate constraint "listing_owners_listing_id_fkey";

alter table "public"."listing_ownership" add constraint "listing_ownership_listing_id_fkey" FOREIGN KEY (listing_id) REFERENCES public.listings(id) ON DELETE CASCADE not valid;

alter table "public"."listing_ownership" validate constraint "listing_ownership_listing_id_fkey";

alter table "public"."listings" add constraint "listings_category_id_fkey" FOREIGN KEY (category_id) REFERENCES public.categories(id) not valid;

alter table "public"."listings" validate constraint "listings_category_id_fkey";

alter table "public"."listings" add constraint "listings_location_id_fkey" FOREIGN KEY (location_id) REFERENCES public.locations(id) not valid;

alter table "public"."listings" validate constraint "listings_location_id_fkey";

alter table "public"."listings" add constraint "listings_parent_listing_id_fkey" FOREIGN KEY (parent_listing_id) REFERENCES public.listings(id) ON DELETE SET NULL not valid;

alter table "public"."listings" validate constraint "listings_parent_listing_id_fkey";

alter table "public"."locations" add constraint "locations_parent_id_fkey" FOREIGN KEY (parent_id) REFERENCES public.locations(id) ON DELETE CASCADE not valid;

alter table "public"."locations" validate constraint "locations_parent_id_fkey";

alter table "public"."payments" add constraint "payments_listing_id_fkey" FOREIGN KEY (listing_id) REFERENCES public.listings(id) ON DELETE SET NULL not valid;

alter table "public"."payments" validate constraint "payments_listing_id_fkey";

alter table "public"."standards" add constraint "standards_category_id_fkey" FOREIGN KEY (category_id) REFERENCES public.categories(id) not valid;

alter table "public"."standards" validate constraint "standards_category_id_fkey";

create or replace view "public"."potential_dead_links" as  SELECT l.id,
    l.business_name,
    l.website,
    c.name AS category,
    count(cl.id) AS click_attempts,
    max(cl.created_at) AS last_attempt,
    l.status
   FROM ((public.listings l
     LEFT JOIN public.clicks cl ON ((l.id = cl.listing_id)))
     LEFT JOIN public.categories c ON ((l.category_id = c.id)))
  WHERE (l.website IS NOT NULL)
  GROUP BY l.id, l.business_name, l.website, c.name, l.status
 HAVING (count(cl.id) > 0)
  ORDER BY (count(cl.id)) DESC;



  create policy "Listing owners can manage their capabilities"
  on "public"."listing_capabilities"
  as permissive
  for all
  to public
using ((listing_id IN ( SELECT listings.id
   FROM public.listings
  WHERE (listings.owner_id = auth.uid()))));



  create policy "Admins can update ownership status"
  on "public"."listing_owners"
  as permissive
  for update
  to public
using ((EXISTS ( SELECT 1
   FROM public.user_profiles
  WHERE ((user_profiles.id = ( SELECT auth.uid() AS uid)) AND (listing_owners.role = 'admin'::text)))));



  create policy "Listing owners can manage their capabilities"
  on "public"."listing_owners"
  as permissive
  for all
  to public
using ((listing_id IN ( SELECT listings.id
   FROM public.listings
  WHERE (listings.owner_id = ( SELECT auth.uid() AS uid)))));



  create policy "Listing owners can update their listings"
  on "public"."listings"
  as permissive
  for update
  to authenticated
using ((id IN ( SELECT listing_ownership.listing_id
   FROM public.listing_ownership
  WHERE ((listing_ownership.user_id = ( SELECT auth.uid() AS uid)) AND (listing_ownership.verified_owner = true)))));


CREATE TRIGGER trigger_update_website_domain BEFORE INSERT OR UPDATE ON public.listings FOR EACH ROW EXECUTE FUNCTION public.update_website_domain();

CREATE TRIGGER update_subscription_invoices_updated_at BEFORE UPDATE ON public.subscription_invoices FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON public.user_profiles FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER on_auth_user_created AFTER INSERT ON auth.users FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();


