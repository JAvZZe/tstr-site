export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "13.0.5"
  }
  public: {
    Tables: {
      blog_posts: {
        Row: {
          author: string | null
          body: string
          canonical_url: string | null
          category: string
          cover_image_url: string | null
          created_at: string | null
          excerpt: string
          id: string
          is_published: boolean | null
          meta_description: string | null
          meta_title: string | null
          published_at: string | null
          reading_time_mins: number | null
          related_listings: string[] | null
          slug: string
          title: string
          updated_at: string | null
        }
        Insert: {
          author?: string | null
          body: string
          canonical_url?: string | null
          category: string
          cover_image_url?: string | null
          created_at?: string | null
          excerpt: string
          id?: string
          is_published?: boolean | null
          meta_description?: string | null
          meta_title?: string | null
          published_at?: string | null
          reading_time_mins?: number | null
          related_listings?: string[] | null
          slug: string
          title: string
          updated_at?: string | null
        }
        Update: {
          author?: string | null
          body?: string
          canonical_url?: string | null
          category?: string
          cover_image_url?: string | null
          created_at?: string | null
          excerpt?: string
          id?: string
          is_published?: boolean | null
          meta_description?: string | null
          meta_title?: string | null
          published_at?: string | null
          reading_time_mins?: number | null
          related_listings?: string[] | null
          slug?: string
          title?: string
          updated_at?: string | null
        }
        Relationships: []
      }
      categories: {
        Row: {
          created_at: string | null
          description: string | null
          display_order: number | null
          icon: string | null
          id: string
          name: string
          parent_id: string | null
          slug: string
          updated_at: string | null
        }
        Insert: {
          created_at?: string | null
          description?: string | null
          display_order?: number | null
          icon?: string | null
          id?: string
          name: string
          parent_id?: string | null
          slug: string
          updated_at?: string | null
        }
        Update: {
          created_at?: string | null
          description?: string | null
          display_order?: number | null
          icon?: string | null
          id?: string
          name?: string
          parent_id?: string | null
          slug?: string
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "categories_parent_id_fkey"
            columns: ["parent_id"]
            isOneToOne: false
            referencedRelation: "categories"
            referencedColumns: ["id"]
          },
        ]
      }
      certifications: {
        Row: {
          confidence: number | null
          created_at: string | null
          expiry_date: string | null
          id: string
          issued_date: string | null
          issuing_body: string | null
          listing_id: string | null
          name: string
          source: string | null
        }
        Insert: {
          confidence?: number | null
          created_at?: string | null
          expiry_date?: string | null
          id?: string
          issued_date?: string | null
          issuing_body?: string | null
          listing_id?: string | null
          name: string
          source?: string | null
        }
        Update: {
          confidence?: number | null
          created_at?: string | null
          expiry_date?: string | null
          id?: string
          issued_date?: string | null
          issuing_body?: string | null
          listing_id?: string | null
          name?: string
          source?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "certifications_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "certifications_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "potential_dead_links"
            referencedColumns: ["id"]
          },
        ]
      }
      claims: {
        Row: {
          business_email: string
          contact_name: string
          created_at: string | null
          id: string
          phone: string | null
          provider_name: string
          status: string | null
          updated_at: string | null
        }
        Insert: {
          business_email: string
          contact_name: string
          created_at?: string | null
          id?: string
          phone?: string | null
          provider_name: string
          status?: string | null
          updated_at?: string | null
        }
        Update: {
          business_email?: string
          contact_name?: string
          created_at?: string | null
          id?: string
          phone?: string | null
          provider_name?: string
          status?: string | null
          updated_at?: string | null
        }
        Relationships: []
      }
      clicks: {
        Row: {
          created_at: string | null
          id: string
          listing_id: string | null
          referrer: string | null
          url: string
          user_agent: string | null
        }
        Insert: {
          created_at?: string | null
          id?: string
          listing_id?: string | null
          referrer?: string | null
          url: string
          user_agent?: string | null
        }
        Update: {
          created_at?: string | null
          id?: string
          listing_id?: string | null
          referrer?: string | null
          url?: string
          user_agent?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "clicks_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "clicks_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "potential_dead_links"
            referencedColumns: ["id"]
          },
        ]
      }
      custom_fields: {
        Row: {
          category_id: string | null
          created_at: string | null
          display_order: number | null
          field_label: string
          field_name: string
          field_type: string
          id: string
          is_required: boolean | null
          is_searchable: boolean | null
          options: Json | null
        }
        Insert: {
          category_id?: string | null
          created_at?: string | null
          display_order?: number | null
          field_label: string
          field_name: string
          field_type: string
          id?: string
          is_required?: boolean | null
          is_searchable?: boolean | null
          options?: Json | null
        }
        Update: {
          category_id?: string | null
          created_at?: string | null
          display_order?: number | null
          field_label?: string
          field_name?: string
          field_type?: string
          id?: string
          is_required?: boolean | null
          is_searchable?: boolean | null
          options?: Json | null
        }
        Relationships: [
          {
            foreignKeyName: "custom_fields_category_id_fkey"
            columns: ["category_id"]
            isOneToOne: false
            referencedRelation: "categories"
            referencedColumns: ["id"]
          },
        ]
      }
      equipment: {
        Row: {
          category: string | null
          confidence: number | null
          created_at: string | null
          id: string
          listing_id: string | null
          manufacturer: string | null
          model: string
          source: string | null
        }
        Insert: {
          category?: string | null
          confidence?: number | null
          created_at?: string | null
          id?: string
          listing_id?: string | null
          manufacturer?: string | null
          model: string
          source?: string | null
        }
        Update: {
          category?: string | null
          confidence?: number | null
          created_at?: string | null
          id?: string
          listing_id?: string | null
          manufacturer?: string | null
          model?: string
          source?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "equipment_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "equipment_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "potential_dead_links"
            referencedColumns: ["id"]
          },
        ]
      }
      leads_rfq: {
        Row: {
          buyer_company: string | null
          buyer_email: string
          buyer_industry: string | null
          buyer_name: string
          buyer_role: string | null
          created_at: string | null
          id: string
          listing_id: string | null
          message: string
          notified_lab: boolean | null
          status: string | null
          updated_at: string | null
        }
        Insert: {
          buyer_company?: string | null
          buyer_email: string
          buyer_industry?: string | null
          buyer_name: string
          buyer_role?: string | null
          created_at?: string | null
          id?: string
          listing_id?: string | null
          message: string
          notified_lab?: boolean | null
          status?: string | null
          updated_at?: string | null
        }
        Update: {
          buyer_company?: string | null
          buyer_email?: string
          buyer_industry?: string | null
          buyer_name?: string
          buyer_role?: string | null
          created_at?: string | null
          id?: string
          listing_id?: string | null
          message?: string
          notified_lab?: boolean | null
          status?: string | null
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "leads_rfq_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "leads_rfq_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "potential_dead_links"
            referencedColumns: ["id"]
          },
        ]
      }
      listing_capabilities: {
        Row: {
          created_at: string | null
          display_order: number | null
          id: string
          listing_id: string
          notes: string | null
          specifications: Json | null
          standard_id: string
          updated_at: string | null
          verified: boolean | null
          verified_at: string | null
          verified_by: string | null
        }
        Insert: {
          created_at?: string | null
          display_order?: number | null
          id?: string
          listing_id: string
          notes?: string | null
          specifications?: Json | null
          standard_id: string
          updated_at?: string | null
          verified?: boolean | null
          verified_at?: string | null
          verified_by?: string | null
        }
        Update: {
          created_at?: string | null
          display_order?: number | null
          id?: string
          listing_id?: string
          notes?: string | null
          specifications?: Json | null
          standard_id?: string
          updated_at?: string | null
          verified?: boolean | null
          verified_at?: string | null
          verified_by?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "listing_capabilities_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "listing_capabilities_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "potential_dead_links"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "listing_capabilities_standard_id_fkey"
            columns: ["standard_id"]
            isOneToOne: false
            referencedRelation: "standards"
            referencedColumns: ["id"]
          },
        ]
      }
      listing_categories: {
        Row: {
          category_id: string | null
          created_at: string | null
          id: string
          is_primary: boolean | null
          listing_id: string | null
        }
        Insert: {
          category_id?: string | null
          created_at?: string | null
          id?: string
          is_primary?: boolean | null
          listing_id?: string | null
        }
        Update: {
          category_id?: string | null
          created_at?: string | null
          id?: string
          is_primary?: boolean | null
          listing_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "listing_categories_category_id_fkey"
            columns: ["category_id"]
            isOneToOne: false
            referencedRelation: "categories"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "listing_categories_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "listing_categories_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "potential_dead_links"
            referencedColumns: ["id"]
          },
        ]
      }
      listing_custom_fields: {
        Row: {
          created_at: string | null
          custom_field_id: string | null
          id: string
          listing_id: string | null
          value: Json
        }
        Insert: {
          created_at?: string | null
          custom_field_id?: string | null
          id?: string
          listing_id?: string | null
          value: Json
        }
        Update: {
          created_at?: string | null
          custom_field_id?: string | null
          id?: string
          listing_id?: string | null
          value?: Json
        }
        Relationships: [
          {
            foreignKeyName: "listing_custom_fields_custom_field_id_fkey"
            columns: ["custom_field_id"]
            isOneToOne: false
            referencedRelation: "custom_fields"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "listing_custom_fields_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "listing_custom_fields_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "potential_dead_links"
            referencedColumns: ["id"]
          },
        ]
      }
      listing_images: {
        Row: {
          created_at: string | null
          display_order: number | null
          id: string
          image_url: string
          is_primary: boolean | null
          listing_id: string | null
        }
        Insert: {
          created_at?: string | null
          display_order?: number | null
          id?: string
          image_url: string
          is_primary?: boolean | null
          listing_id?: string | null
        }
        Update: {
          created_at?: string | null
          display_order?: number | null
          id?: string
          image_url?: string
          is_primary?: boolean | null
          listing_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "listing_images_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "listing_images_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "potential_dead_links"
            referencedColumns: ["id"]
          },
        ]
      }
      listing_owners: {
        Row: {
          created_at: string | null
          id: string
          listing_id: string
          role: string
          status: string
          token_expires_at: string | null
          updated_at: string | null
          user_id: string
          verification_method: string | null
          verification_token: string | null
          verified_at: string | null
        }
        Insert: {
          created_at?: string | null
          id?: string
          listing_id: string
          role?: string
          status?: string
          token_expires_at?: string | null
          updated_at?: string | null
          user_id: string
          verification_method?: string | null
          verification_token?: string | null
          verified_at?: string | null
        }
        Update: {
          created_at?: string | null
          id?: string
          listing_id?: string
          role?: string
          status?: string
          token_expires_at?: string | null
          updated_at?: string | null
          user_id?: string
          verification_method?: string | null
          verification_token?: string | null
          verified_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "listing_owners_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "listing_owners_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "potential_dead_links"
            referencedColumns: ["id"]
          },
        ]
      }
      listing_ownership: {
        Row: {
          claimed_at: string
          created_at: string
          id: string
          listing_id: string
          user_id: string
          verification_method: string | null
          verified_at: string | null
          verified_by: string | null
          verified_owner: boolean
        }
        Insert: {
          claimed_at?: string
          created_at?: string
          id?: string
          listing_id: string
          user_id: string
          verification_method?: string | null
          verified_at?: string | null
          verified_by?: string | null
          verified_owner?: boolean
        }
        Update: {
          claimed_at?: string
          created_at?: string
          id?: string
          listing_id?: string
          user_id?: string
          verification_method?: string | null
          verified_at?: string | null
          verified_by?: string | null
          verified_owner?: boolean
        }
        Relationships: [
          {
            foreignKeyName: "listing_ownership_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "listing_ownership_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "potential_dead_links"
            referencedColumns: ["id"]
          },
        ]
      }
      listing_premium_data: {
        Row: {
          created_at: string
          crunchbase_url: string | null
          email: string | null
          id: string
          linkedin_url: string | null
          listing_id: string | null
          updated_at: string
        }
        Insert: {
          created_at?: string
          crunchbase_url?: string | null
          email?: string | null
          id?: string
          linkedin_url?: string | null
          listing_id?: string | null
          updated_at?: string
        }
        Update: {
          created_at?: string
          crunchbase_url?: string | null
          email?: string | null
          id?: string
          linkedin_url?: string | null
          listing_id?: string | null
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "listing_premium_data_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "listing_premium_data_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "potential_dead_links"
            referencedColumns: ["id"]
          },
        ]
      }
      listings: {
        Row: {
          address: string | null
          billing_tier: string | null
          business_name: string
          category_id: string
          category_slug: string | null
          claimed: boolean | null
          claimed_at: string | null
          contact_email: string | null
          contact_visibility: string | null
          created_at: string | null
          description: string | null
          email: string | null
          featured: boolean
          featured_until: string | null
          id: string
          is_featured: boolean | null
          latitude: number | null
          location_id: string
          longitude: number | null
          outreach_sent_at: string | null
          owner_id: string | null
          parent_listing_id: string | null
          phone: string | null
          plan_type: string | null
          priority_rank: number
          published_at: string | null
          region: string | null
          script_location: string | null
          slug: string
          source_script: string | null
          status: string | null
          trust_score: number | null
          updated_at: string | null
          verified: boolean | null
          views: number | null
          website: string | null
          website_domain: string | null
        }
        Insert: {
          address?: string | null
          billing_tier?: string | null
          business_name: string
          category_id: string
          category_slug?: string | null
          claimed?: boolean | null
          claimed_at?: string | null
          contact_email?: string | null
          contact_visibility?: string | null
          created_at?: string | null
          description?: string | null
          email?: string | null
          featured?: boolean
          featured_until?: string | null
          id?: string
          is_featured?: boolean | null
          latitude?: number | null
          location_id: string
          longitude?: number | null
          outreach_sent_at?: string | null
          owner_id?: string | null
          parent_listing_id?: string | null
          phone?: string | null
          plan_type?: string | null
          priority_rank?: number
          published_at?: string | null
          region?: string | null
          script_location?: string | null
          slug: string
          source_script?: string | null
          status?: string | null
          trust_score?: number | null
          updated_at?: string | null
          verified?: boolean | null
          views?: number | null
          website?: string | null
          website_domain?: string | null
        }
        Update: {
          address?: string | null
          billing_tier?: string | null
          business_name?: string
          category_id?: string
          category_slug?: string | null
          claimed?: boolean | null
          claimed_at?: string | null
          contact_email?: string | null
          contact_visibility?: string | null
          created_at?: string | null
          description?: string | null
          email?: string | null
          featured?: boolean
          featured_until?: string | null
          id?: string
          is_featured?: boolean | null
          latitude?: number | null
          location_id?: string
          longitude?: number | null
          outreach_sent_at?: string | null
          owner_id?: string | null
          parent_listing_id?: string | null
          phone?: string | null
          plan_type?: string | null
          priority_rank?: number
          published_at?: string | null
          region?: string | null
          script_location?: string | null
          slug?: string
          source_script?: string | null
          status?: string | null
          trust_score?: number | null
          updated_at?: string | null
          verified?: boolean | null
          views?: number | null
          website?: string | null
          website_domain?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "listings_category_id_fkey"
            columns: ["category_id"]
            isOneToOne: false
            referencedRelation: "categories"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "listings_location_id_fkey"
            columns: ["location_id"]
            isOneToOne: false
            referencedRelation: "locations"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "listings_parent_listing_id_fkey"
            columns: ["parent_listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "listings_parent_listing_id_fkey"
            columns: ["parent_listing_id"]
            isOneToOne: false
            referencedRelation: "potential_dead_links"
            referencedColumns: ["id"]
          },
        ]
      }
      locations: {
        Row: {
          created_at: string | null
          id: string
          latitude: number | null
          level: string
          longitude: number | null
          name: string
          parent_id: string | null
          slug: string
          updated_at: string | null
        }
        Insert: {
          created_at?: string | null
          id?: string
          latitude?: number | null
          level: string
          longitude?: number | null
          name: string
          parent_id?: string | null
          slug: string
          updated_at?: string | null
        }
        Update: {
          created_at?: string | null
          id?: string
          latitude?: number | null
          level?: string
          longitude?: number | null
          name?: string
          parent_id?: string | null
          slug?: string
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "locations_parent_id_fkey"
            columns: ["parent_id"]
            isOneToOne: false
            referencedRelation: "locations"
            referencedColumns: ["id"]
          },
        ]
      }
      payment_history: {
        Row: {
          amount: number
          created_at: string | null
          currency: string | null
          description: string | null
          id: string
          paypal_subscription_id: string | null
          paypal_transaction_id: string | null
          status: string
          tier: string
          user_id: string | null
        }
        Insert: {
          amount: number
          created_at?: string | null
          currency?: string | null
          description?: string | null
          id?: string
          paypal_subscription_id?: string | null
          paypal_transaction_id?: string | null
          status: string
          tier: string
          user_id?: string | null
        }
        Update: {
          amount?: number
          created_at?: string | null
          currency?: string | null
          description?: string | null
          id?: string
          paypal_subscription_id?: string | null
          paypal_transaction_id?: string | null
          status?: string
          tier?: string
          user_id?: string | null
        }
        Relationships: []
      }
      payments: {
        Row: {
          amount: number
          created_at: string | null
          currency: string | null
          id: string
          listing_id: string | null
          notes: string | null
          owner_id: string | null
          payment_method: string | null
          proof_image_url: string | null
          reference_number: string | null
          status: string | null
          verified_at: string | null
          verified_by: string | null
        }
        Insert: {
          amount: number
          created_at?: string | null
          currency?: string | null
          id?: string
          listing_id?: string | null
          notes?: string | null
          owner_id?: string | null
          payment_method?: string | null
          proof_image_url?: string | null
          reference_number?: string | null
          status?: string | null
          verified_at?: string | null
          verified_by?: string | null
        }
        Update: {
          amount?: number
          created_at?: string | null
          currency?: string | null
          id?: string
          listing_id?: string | null
          notes?: string | null
          owner_id?: string | null
          payment_method?: string | null
          proof_image_url?: string | null
          reference_number?: string | null
          status?: string | null
          verified_at?: string | null
          verified_by?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "payments_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "payments_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "potential_dead_links"
            referencedColumns: ["id"]
          },
        ]
      }
      pending_research: {
        Row: {
          address: string | null
          business_name: string
          category: string | null
          created_at: string | null
          description: string | null
          email: string | null
          id: string
          location_id: string | null
          notes: string | null
          original_id: string | null
          phone: string | null
          researched_at: string | null
          researched_by: string | null
          status: string | null
          updated_at: string | null
          validation_error: string | null
          website: string | null
        }
        Insert: {
          address?: string | null
          business_name: string
          category?: string | null
          created_at?: string | null
          description?: string | null
          email?: string | null
          id?: string
          location_id?: string | null
          notes?: string | null
          original_id?: string | null
          phone?: string | null
          researched_at?: string | null
          researched_by?: string | null
          status?: string | null
          updated_at?: string | null
          validation_error?: string | null
          website?: string | null
        }
        Update: {
          address?: string | null
          business_name?: string
          category?: string | null
          created_at?: string | null
          description?: string | null
          email?: string | null
          id?: string
          location_id?: string | null
          notes?: string | null
          original_id?: string | null
          phone?: string | null
          researched_at?: string | null
          researched_by?: string | null
          status?: string | null
          updated_at?: string | null
          validation_error?: string | null
          website?: string | null
        }
        Relationships: []
      }
      rfq_leads: {
        Row: {
          buyer_company: string | null
          buyer_email: string
          buyer_name: string | null
          created_at: string | null
          id: string
          listing_id: string | null
          standards_needed: string[] | null
          status: string | null
          test_description: string | null
        }
        Insert: {
          buyer_company?: string | null
          buyer_email: string
          buyer_name?: string | null
          created_at?: string | null
          id?: string
          listing_id?: string | null
          standards_needed?: string[] | null
          status?: string | null
          test_description?: string | null
        }
        Update: {
          buyer_company?: string | null
          buyer_email?: string
          buyer_name?: string | null
          created_at?: string | null
          id?: string
          listing_id?: string | null
          standards_needed?: string[] | null
          status?: string | null
          test_description?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "rfq_leads_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "rfq_leads_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "potential_dead_links"
            referencedColumns: ["id"]
          },
        ]
      }
      schema_migrations: {
        Row: {
          applied_at: string
          name: string
          version: number
        }
        Insert: {
          applied_at?: string
          name: string
          version: number
        }
        Update: {
          applied_at?: string
          name?: string
          version?: number
        }
        Relationships: []
      }
      search_logs: {
        Row: {
          created_at: string | null
          filters: Json | null
          id: string
          ip_hash: string | null
          query: string | null
          results_count: number | null
        }
        Insert: {
          created_at?: string | null
          filters?: Json | null
          id?: string
          ip_hash?: string | null
          query?: string | null
          results_count?: number | null
        }
        Update: {
          created_at?: string | null
          filters?: Json | null
          id?: string
          ip_hash?: string | null
          query?: string | null
          results_count?: number | null
        }
        Relationships: []
      }
      standards: {
        Row: {
          category_id: string | null
          code: string
          created_at: string | null
          description: string | null
          description_long: string | null
          id: string
          is_active: boolean | null
          issuing_body: string | null
          meta_description: string | null
          meta_title: string | null
          name: string
          page_published: boolean | null
          related_equipment: string[] | null
          revision: string | null
          slug: string | null
          standard_type: string | null
          typical_industries: string[] | null
          updated_at: string | null
          url: string | null
        }
        Insert: {
          category_id?: string | null
          code: string
          created_at?: string | null
          description?: string | null
          description_long?: string | null
          id?: string
          is_active?: boolean | null
          issuing_body?: string | null
          meta_description?: string | null
          meta_title?: string | null
          name: string
          page_published?: boolean | null
          related_equipment?: string[] | null
          revision?: string | null
          slug?: string | null
          standard_type?: string | null
          typical_industries?: string[] | null
          updated_at?: string | null
          url?: string | null
        }
        Update: {
          category_id?: string | null
          code?: string
          created_at?: string | null
          description?: string | null
          description_long?: string | null
          id?: string
          is_active?: boolean | null
          issuing_body?: string | null
          meta_description?: string | null
          meta_title?: string | null
          name?: string
          page_published?: boolean | null
          related_equipment?: string[] | null
          revision?: string | null
          slug?: string | null
          standard_type?: string | null
          typical_industries?: string[] | null
          updated_at?: string | null
          url?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "standards_category_id_fkey"
            columns: ["category_id"]
            isOneToOne: false
            referencedRelation: "categories"
            referencedColumns: ["id"]
          },
        ]
      }
      subscription_invoices: {
        Row: {
          admin_notes: string | null
          amount: number
          created_at: string
          currency: string
          due_date: string
          id: string
          invoice_date: string
          notes: string | null
          paid_date: string | null
          payment_method: string | null
          payment_reference: string | null
          status: string
          tier: string
          updated_at: string
          user_id: string
        }
        Insert: {
          admin_notes?: string | null
          amount: number
          created_at?: string
          currency?: string
          due_date: string
          id?: string
          invoice_date?: string
          notes?: string | null
          paid_date?: string | null
          payment_method?: string | null
          payment_reference?: string | null
          status?: string
          tier: string
          updated_at?: string
          user_id: string
        }
        Update: {
          admin_notes?: string | null
          amount?: number
          created_at?: string
          currency?: string
          due_date?: string
          id?: string
          invoice_date?: string
          notes?: string | null
          paid_date?: string | null
          payment_method?: string | null
          payment_reference?: string | null
          status?: string
          tier?: string
          updated_at?: string
          user_id?: string
        }
        Relationships: []
      }
      user_profiles: {
        Row: {
          billing_email: string | null
          company_name: string | null
          created_at: string
          id: string
          industry: string | null
          last_payment_date: string | null
          payment_method: string | null
          paypal_subscription_id: string | null
          role: string | null
          subscription_end_date: string | null
          subscription_start_date: string | null
          subscription_status: string
          subscription_tier: string
          updated_at: string
          user_type: string | null
        }
        Insert: {
          billing_email?: string | null
          company_name?: string | null
          created_at?: string
          id: string
          industry?: string | null
          last_payment_date?: string | null
          payment_method?: string | null
          paypal_subscription_id?: string | null
          role?: string | null
          subscription_end_date?: string | null
          subscription_start_date?: string | null
          subscription_status?: string
          subscription_tier?: string
          updated_at?: string
          user_type?: string | null
        }
        Update: {
          billing_email?: string | null
          company_name?: string | null
          created_at?: string
          id?: string
          industry?: string | null
          last_payment_date?: string | null
          payment_method?: string | null
          paypal_subscription_id?: string | null
          role?: string | null
          subscription_end_date?: string | null
          subscription_start_date?: string | null
          subscription_status?: string
          subscription_tier?: string
          updated_at?: string
          user_type?: string | null
        }
        Relationships: []
      }
      verification_evidence: {
        Row: {
          created_at: string | null
          file_type: string | null
          file_url: string
          id: string
          listing_id: string | null
          uploaded_by: string | null
          verified: boolean | null
        }
        Insert: {
          created_at?: string | null
          file_type?: string | null
          file_url: string
          id?: string
          listing_id?: string | null
          uploaded_by?: string | null
          verified?: boolean | null
        }
        Update: {
          created_at?: string | null
          file_type?: string | null
          file_url?: string
          id?: string
          listing_id?: string | null
          uploaded_by?: string | null
          verified?: boolean | null
        }
        Relationships: [
          {
            foreignKeyName: "verification_evidence_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "verification_evidence_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "potential_dead_links"
            referencedColumns: ["id"]
          },
        ]
      }
      waitlist: {
        Row: {
          created_at: string | null
          email: string
          id: string
          notes: string | null
          source: string | null
          status: string | null
        }
        Insert: {
          created_at?: string | null
          email: string
          id?: string
          notes?: string | null
          source?: string | null
          status?: string | null
        }
        Update: {
          created_at?: string | null
          email?: string
          id?: string
          notes?: string | null
          source?: string | null
          status?: string | null
        }
        Relationships: []
      }
    }
    Views: {
      potential_dead_links: {
        Row: {
          business_name: string | null
          category: string | null
          click_attempts: number | null
          id: string | null
          last_attempt: string | null
          status: string | null
          website: string | null
        }
        Relationships: []
      }
    }
    Functions: {
      calculate_listing_billing: {
        Args: { p_listing_id: string }
        Returns: Json
      }
      calculate_trust_score: { Args: { p_listing_id: string }; Returns: number }
      can_auto_claim: {
        Args: { listing_website: string; user_email: string }
        Returns: boolean
      }
      can_view_contact_info: { Args: { user_uuid: string }; Returns: boolean }
      extract_domain: { Args: { url: string }; Returns: string }
      get_click_stats: {
        Args: { days_back?: number }
        Returns: {
          clicks: number
          date: string
          unique_listings: number
        }[]
      }
      get_top_clicked_listings: {
        Args: { limit_count?: number }
        Returns: {
          business_name: string
          category_name: string
          clicks: number
          last_click: string
          listing_id: string
          website: string
        }[]
      }
      get_user_tier: { Args: { user_uuid: string }; Returns: string }
      make_user_admin: { Args: { user_email: string }; Returns: boolean }
      search_by_standard: {
        Args: {
          p_category_id?: string
          p_min_specs?: Json
          p_standard_code: string
        }
        Returns: {
          business_name: string
          listing_id: string
          specifications: Json
          standard_code: string
          standard_name: string
          website: string
        }[]
      }
      user_owns_listing: {
        Args: { listing_uuid: string; user_uuid: string }
        Returns: boolean
      }
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {},
  },
} as const
