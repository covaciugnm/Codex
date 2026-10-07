-- Stop with an actionable error if an earlier direct SQL edit exceeded the
-- JSON consumer's finite-number range. Never replace existing values silently.
DO $$
DECLARE invalid_key text;
BEGIN
  SELECT key INTO invalid_key FROM content_variables
  WHERE CASE WHEN jsonb_typeof(value) = 'number'
    THEN NOT ((value #>> '{}')::numeric BETWEEN -1.7976931348623157e308::numeric AND 1.7976931348623157e308::numeric)
    ELSE false END
  LIMIT 1;
  IF invalid_key IS NOT NULL THEN
    RAISE EXCEPTION 'Variable "%" exceeds the finite JSON number range; correct this value explicitly, then rerun migration 003', invalid_key
      USING ERRCODE = '23514';
  END IF;
END;
$$;

ALTER TABLE content_variables ADD CONSTRAINT content_variables_finite_number
CHECK (CASE WHEN jsonb_typeof(value) = 'number'
  THEN (value #>> '{}')::numeric BETWEEN -1.7976931348623157e308::numeric AND 1.7976931348623157e308::numeric
  ELSE true END);
