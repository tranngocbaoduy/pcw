SET collation_connection = 'utf8_general_ci';

ALTER DATABASE xpcwstor_prod CHARACTER SET utf8 COLLATE utf8_general_ci;

ALTER TABLE auth_group CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE auth_group_permissions CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE auth_permission CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE auth_user CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE auth_user_groups CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE auth_user_user_permissions CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE crawler_category CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE crawler_groupproduct CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE crawler_historypricing CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE crawler_pageinfo CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE crawler_parser CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE crawler_product CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE crawler_sitemap CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE crawler_scraper CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE crawler_scrapersitemap CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE crawler_wareparser CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE django_admin_log CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE django_content_type CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE django_migrations CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE django_session CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci; 
 

