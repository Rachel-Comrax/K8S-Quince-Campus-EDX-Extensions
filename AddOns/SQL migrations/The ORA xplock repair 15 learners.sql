-- This script fix ORA issues for specific learners that their answer's
-- json was broken. The script fix the selected answer and then customer success or support can delete the answers from the UI.
-- Date: 04/01/2023
-- Owner: Vladimir

-- #1
SELECT *
FROM edxapp.submissions_submission
WHERE uuid = 'e1fd8aefe5ef4e1c957bdbbc2cbd5ea6';

UPDATE edxapp.submissions_submission 
SET raw_answer = '{"parts":[{"text":"התשובה בטבלה"}],"file_keys":[],"files_descriptions":[],"files_names":[],"files_sizes":[]}'
WHERE uuid = 'e1fd8aefe5ef4e1c957bdbbc2cbd5ea6';

-- #2
SELECT *
FROM edxapp.submissions_submission
WHERE uuid = '9f9776222ee64ec7b57369bb55e7726f';

UPDATE edxapp.submissions_submission 
SET raw_answer = '{"parts":[{"text":""}],"file_keys":[],"files_descriptions":[],"files_names":[],"files_sizes":[]}'
WHERE uuid = '9f9776222ee64ec7b57369bb55e7726f';

-- #3
SELECT *
FROM edxapp.submissions_submission
WHERE uuid = '58d6e05d757944d29a80d0058e2aa098';

UPDATE edxapp.submissions_submission 
SET raw_answer = '{"parts":[{"text":""}],"file_keys":[],"files_descriptions":[],"files_names":[],"files_sizes":[]}'
WHERE uuid = '58d6e05d757944d29a80d0058e2aa098';

-- #4
SELECT *
FROM edxapp.submissions_submission
WHERE uuid = '50d364bf401042b19b2a8b414335ee4d';

UPDATE edxapp.submissions_submission 
SET raw_answer = '{"parts":[{"text":"המצגת שלי!!!❤❤❤❤❤❤❤"}],"file_keys":[],"files_descriptions":[],"files_names":[],"files_sizes":[]}'
WHERE uuid = '50d364bf401042b19b2a8b414335ee4d';

-- #5
SELECT *
FROM edxapp.submissions_submission
WHERE uuid = '1567b91279794e5395dfc591f2a9bfd5';

UPDATE edxapp.submissions_submission 
SET raw_answer = '{"parts":[{"text":"Dingy dingy dingy dingy"}],"file_keys":[],"files_descriptions":[],"files_names":[],"files_sizes":[]}'
WHERE uuid = '1567b91279794e5395dfc591f2a9bfd5';

-- #6
SELECT *
FROM edxapp.submissions_submission
WHERE uuid = '5b8536c1469f45f88c7fa53a845d1e27';

UPDATE edxapp.submissions_submission 
SET raw_answer = '{"parts":[{"text":"ועידת קטוביץ\'-אביאל רוד"}],"file_keys":[],"files_descriptions":[],"files_names":[],"files_sizes":[]}'
WHERE uuid = '5b8536c1469f45f88c7fa53a845d1e27';


-- #7
SELECT *
FROM edxapp.submissions_submission
WHERE uuid = '251f2cfe73b540deb7c6a354b92a9a92';

UPDATE edxapp.submissions_submission 
SET raw_answer = '{"parts":[{"text":"שלושה תחומים שהמהפיכה המדעית שינתה:  1. טכנולוגיה"}],"file_keys":[],"files_descriptions":[],"files_names":[],"files_sizes":[]}'
WHERE uuid = '251f2cfe73b540deb7c6a354b92a9a92';


-- #8
SELECT *
FROM edxapp.submissions_submission
WHERE uuid = '373eba56aeb54822b4c69daa34d87558';

UPDATE edxapp.submissions_submission 
SET raw_answer = '{"parts":[{"text":"1.א.\'המפעל שלנו הצליח אך ורק משום שעמד תמיד בחזית הטכנולוגית של התקופה המודרנית.\'  תיאור על מצב הצלחת המדינה מפני הצלחותיה בתחום הטכנולוגי - מודרני    ב.\'עלינו לתפוס את ארצנו במלוא יופייה הטבעי ולפתח אותה בהתאם. הארץ צריכה להיות קודם כל יפה, ובכל מקום. היופי תמיד משמח לב אנוש.\'  תיאור תפיסה מתוקנת מציגה את הערכתינו ליופייה של הארץ. גישתנו לחשיבות יופייה וצעדים שנוקטים לפיתוחה לפי תפיסה זו, ובונוס שזוכים אנו אם ננקוט בצעדים נכונים אלא.    ג. \'לא רק מתוך דבקות ב\'ואהבת לרעך כמוך\' אנחנו חייבים להגיד לבאים: בן אדם, אחי אתה. זה הרי רק לטובתנו!... כל מה שנטעתם במקום הזה יהיה חסר ערך ויקמול, אם חופש המחשבה והביטוי, הנדיבות ואהבת הבריות לא יפרחו בו.\'  תיאור ערכים חיונים במדינה שבלעדיהם התוצרים, העתיד ופירות העמל יהיו חסרי ערך.    2. א. https://www.globes.co.il/news/article.aspx?did=1001331373 - סטארט-אפ  מחקר: ישראל במקום השלישי בדירוג האקוסיסטמים הטכנולוגיים המובילים    ב. https://www.teva.org.il/vision - חזון החברה להגנת הטבע"}],"file_keys":[],"files_descriptions":[],"files_names":[],"files_sizes":[]}'
WHERE uuid = '373eba56aeb54822b4c69daa34d87558';

-- #9
SELECT *
FROM edxapp.submissions_submission
WHERE uuid = 'd617306cadee4b78bca9fd283601a29a';

UPDATE edxapp.submissions_submission 
SET raw_answer = '{"parts":[{"text":"[08:30, 12/12/2022] נתנאל פדידה נציג תמיכה טכנית: יורד  [11:01, 12/12/2022] Eli"}],"file_keys":[],"files_descriptions":[],"files_names":[],"files_sizes":[]}'
WHERE uuid = 'd617306cadee4b78bca9fd283601a29a';

-- #10
SELECT *
FROM edxapp.submissions_submission
WHERE uuid = 'b48f1e9c28e546508ca9df86d8199fc5';

UPDATE edxapp.submissions_submission 
SET raw_answer = '{"parts":[{"text":""}],"file_keys":[],"files_descriptions":[],"files_names":[],"files_sizes":[]}'
WHERE uuid = 'b48f1e9c28e546508ca9df86d8199fc5';

-- #11
SELECT *
FROM edxapp.submissions_submission
WHERE uuid = '26e954c1fb884a8bbf8fbbc2cd1fb505';

UPDATE edxapp.submissions_submission 
SET raw_answer = '{"parts":[{"text":"המורה חגית המושלמת הגשתי לך את המצגת בוואטסאפ."}],"file_keys":[],"files_descriptions":[],"files_names":[],"files_sizes":[]}'
WHERE uuid = '26e954c1fb884a8bbf8fbbc2cd1fb505';

-- #12
SELECT *
FROM edxapp.submissions_submission
WHERE uuid = '3556feaf496946e2812841329ee4e4f0';

UPDATE edxapp.submissions_submission 
SET raw_answer = '{"parts":[{"text":"המצגת מחכה בקבצים"}],"file_keys":[],"files_descriptions":[],"files_names":[],"files_sizes":[]}'
WHERE uuid = '3556feaf496946e2812841329ee4e4f0';

-- #13
SELECT *
FROM edxapp.submissions_submission
WHERE uuid = 'cf8c1f191885493786a3993424bd22ac';

UPDATE edxapp.submissions_submission 
SET raw_answer = '{"parts":[{"text":"עומדת בפנינו סוגייה חשובה ובה עוסקים בשאלה האם יש צורך לאשר או לדחות את סעיף 4 א בהצעת התיקון לחוק השבות.   עמדתי היא שהצעת חוק המאפשרת עלייה של ילדים ונכדים ובני זוג של יהודים צריכה להידחות מפני שני סיבות עיקריות, האחת והחשובה ביותר היא שנפתחת דלת לעלייה המונית של בני אדם אשר אינם באמת יהודים ע\'פ ההלכה היהודית ובכך מכניסים את סכנת ההתבוללות של נישואי תערובת האסורה ע\'פ התורה.  יהודי אשר נולד לאימא יהודייה ונישא לגויה ונולד להם ילד על פי ההלכה היהודית אותו ילד נחשב לגוי גמור ואסור בנישואים עם יהודייה ,בכך שהצעת החוק מחשיבה אותו ליהודי ניתנת בפניו אפשרות לעלות ארצה ולהתחנך במוסדות יהודיים ולהתערב בחברה הצעירה ובכך גובר הסיכוי שיהודייה תתחתן עמו למרות האיסור ותגרום להתבוללות קשה בארץ, ההתבוללות תיווצר גם ע\'י הכרה ביהודי שגויר בגיור רפורמי גיור זה לא נחשב גיור כהלכה ע\'פ התורה ולכן אותו אדם נשאר בסטטוס גוי ואסור באסור גמור להתחתן עם בת יהודייה, יוסי שריד, מתוך ועל בסיס \'שבועות החג היפה ביותר\' מביא עמדה מנוגדת לשלי ובה טוען ש\'כל אדם אשר  יבוא ויודיע - באשר תלכי אלך ובאשר תליני אלין וגו\' - יוכל להישאר אתנו ולבוא בקהלנו  למרות שלא עבר הליכי גיור לחומרה\'. זוהי דעה מסולפת לגמרי מכיוון שרות כן עברה גיור כהלכה כפי שכתוב בחז\'ל(זוהר החדש דף ע\'ט עמוד א) והגר\'א.   סיבה נוספת התומכת בעמדה לדחיית הצעת החוק היא שהעלייה בעקבות כך  לארץ תיהיה המונית. כי כאשר ניתנת פרשנות רחבה למילה יהודי אנשים רבים נכנסים תחת קטגוריה זו.   כפי שאמר שר העלייה חיים משה שפירא בדיון בממשלה שעלייה המונית כזאת \'מובילה אותנו לקטסטרופה ולכן חייבת להיות רגולציה. צריך שיהיה עלייה אך עלייה מכוונת\' הפתרון הוא  שהרגולציה תהיה בכך שניתן פרשנות צרה למונח יהודי רק ע\'פ מורשת ישראל, התורה . יהודי בן לאימא יהודייה בלבד.  בדיקה נעימה"}],"file_keys":[],"files_descriptions":[],"files_names":[],"files_sizes":[]}'
WHERE uuid = 'cf8c1f191885493786a3993424bd22ac';

-- #14
SELECT *
FROM edxapp.submissions_submission
WHERE uuid = 'f704fd2c93564be9b9fc83e0236c4c3a';

UPDATE edxapp.submissions_submission 
SET raw_answer = '{"parts":[{"text":"התנועה הציונית והרצל בחרתי את הנושא הזה בגלל שהרצל הוא באמת היה האדם הזה שיעשה הכל בשביל המדינה שלו ולמרות כל הכישלונות שקרו הוא לא וויתר עד שתקום מדינה יהודית למרות שהוא לא זכה לראות את קום המדינה כולנו מעריכים אותו ובגלל זה בחרתי את הנושא הזה.    לי היה כיף שלמדנו במחשב בגלל שזה לא רגיל שלומדים פתאום מקצוע רק במחשב אז זה כיף לעשות את השינוי הזה וגם היה כיף ללמוד ככה עם כל הכיתה"}],"file_keys":[],"files_descriptions":[],"files_names":[],"files_sizes":[]}'
WHERE uuid = 'f704fd2c93564be9b9fc83e0236c4c3a';

-- #15
SELECT *
FROM edxapp.submissions_submission
WHERE uuid = 'f3804279b08444448166019b72279ae3';

UPDATE edxapp.submissions_submission 
SET raw_answer = '{"parts":[{"text":"בקריקטורה השניה מראים לנו בעצם את היהודי בתור אדם חלש כשהנאצי תופס אותו ואם הנאצי לא יעשה משהו היהודים השתלטו על העולם ובעצם יהרסו אותו\n\nבקריקטורה השלישית בעצם מנסים להראות לנו איך אמור להראות הגזע הארי ושהגזע הארי אמור להיות בלונדיני כמו היטלר והיטלר לא בלונדיני, גם כתוב שצריך להיות רזה כמו גרינג והוא לא יפה וצריך להיות יפה כמו גלבס אבל גלאבס לא באמת יפה."}],"file_keys":[],"files_descriptions":[],"files_names":[],"files_sizes":[]}'
WHERE uuid = 'f3804279b08444448166019b72279ae3';

commit;
