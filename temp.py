print "Installing JDBC provider..."

AdminJDBC.createJDBCProvider("DefaultNode01", "server1", "PostgreSQL JDBC Provider", "org.postgresql.jdbc2.optional.ConnectionPool", "classpath=${CUST_PATH}/postgresql-9.4-1206-jdbc42.jar, description='PostgreSQL JDBC Provider', providerType='PostgreSQL JDBC Driver Provider'") 
AdminConfig.save()

print "Installing J2C Auth data..."

security = AdminConfig.getid('/Cell:DefaultCell01/Security:/')
print security
alias = ['alias', 'DefaultNode01/postgreAuth']
userid = ['userId', 'ibm_cloud_9b4b8a88_9f9b_4687_a36d_9099038efbae']
password = ['password', 'dae62724fbf067a147103b334b361e6323e006aa75f3647efaed1660314d5ae6']
jaasAttrs = [alias, userid, password]
print jaasAttrs
AdminConfig.create('JAASAuthData', security, jaasAttrs)
AdminConfig.save()
