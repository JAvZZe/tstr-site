// Run with: node --experimental-strip-types src/lib/validate.test.ts
// (or compile via the project's ts toolchain). Validates the boundary-validation
// helper used by contact/newsletter/submit API routes.
import { requiredString, optionalString, validateJson } from './validate.ts';

let pass = 0, fail = 0;
function check(name: string, cond: boolean) {
  if (cond) { pass++; console.log(`  ok  ${name}`); }
  else { fail++; console.log(`FAIL  ${name}`); }
}

// requiredString
check('rejects empty', !requiredString('', 'x').ok);
check('rejects non-string', !requiredString(123, 'x').ok);
check('rejects over-max', !requiredString('a'.repeat(201), 'x', { max: 200 }).ok);
check('accepts valid', requiredString('hi', 'x', { max: 200 }).ok);
check('rejects bad email', !requiredString('notanemail', 'e', { email: true }).ok);
check('accepts good email', requiredString('a@b.co', 'e', { email: true }).ok);

// optionalString
check('optional empty -> ""', optionalString(undefined) === '');
check('optional trims+clamps', optionalString('  x'.padEnd(300, 'y'), { max: 5 }) === 'x'.padEnd(5, 'y'));

// validateJson
const bad = validateJson('{not json', () => ({ ok: true, data: {} as any }));
check('validateJson rejects bad json', !bad.ok);
const notObj = validateJson('[1,2]', () => ({ ok: true, data: {} as any }));
check('validateJson rejects non-object', !notObj.ok);
const good = validateJson('{"email":"a@b.co"}', (b: any) => {
  const r = requiredString(b.email, 'Email', { email: true });
  return r.ok ? { ok: true, data: { email: r.data } } : { ok: false, error: r.error };
});
check('validateJson accepts good', good.ok && (good as any).data.email === 'a@b.co');

console.log(`\n${pass} passed, ${fail} failed`);
if (fail > 0) process.exit(1);
