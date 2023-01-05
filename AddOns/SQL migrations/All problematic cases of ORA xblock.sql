-- This script find ORA issues for specific learners that their answer's json was broken.
-- Date: 04/01/2023
-- Owner: Vladimir

-- All problematic cases of ORA xblock
-- SELECT SSUB.id, SSUB.submitted_at, SSUB.raw_answer, SSTU.course_id, SSTU.item_id, SSTU.item_type
SELECT *
FROM edxapp.submissions_submission as SSUB
LEFT JOIN edxapp.submissions_studentitem as SSTU
	ON SSTU.id = SSUB.student_item_id
LEFT JOIN edxapp.student_anonymoususerid as ANON
	ON ANON.anonymous_user_id = SSTU.student_id
LEFT JOIN edxapp.auth_user as AUTH
	ON AUTH.id= ANON.user_id
-- WHERE ANON.anonymous_user_id = '17f2f0f8588cc4895147efff8468b741'
-- WHERE uuid like '%dcf096f2%'
WHERE raw_answer like '{%' AND raw_answer not like '%}';