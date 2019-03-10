import sys
import os

global  AdminConfig

def getNodeId (prompt):
    nodeList = AdminConfig.list("Node").split("\n")

    if (len(nodeList) == 1):
        node = nodeList[0]
    else:
        print ""
        print "Available Nodes:"

        nodeNameList = []

        for item in nodeList:
            item = item.rstrip()
            name = getName(item) 

            nodeNameList.append(name)
            print "   " + name

        DefaultNode = nodeNameList[0]
        if (prompt == ""):
            prompt = "Select the desired node"

        nodeName = getValidInput(prompt+" ["+DefaultNode+"]:", DefaultNode, nodeNameList )

        index = nodeNameList.index(nodeName)
        node = nodeList[index]

    return node


def getServerId (prompt):
    serverList = AdminConfig.list("Server").split("\n")

    if (len(serverList) == 1):
        server = serverList[0]
    else:
        print ""
        print "Available Servers:"

        serverNameList = []

        for item in serverList:
            item = item.rstrip()
            name = getName(item)

            serverNameList.append(name)
            print "   " + name

        DefaultServer = serverNameList[0]
        if (prompt == ""):
            prompt = "Select the desired server"
        serverName = getValidInput(prompt+" ["+DefaultServer+"]:", DefaultServer, serverNameList )

        index = serverNameList.index(serverName)
        server = serverList[index]

    return server


def getName (objectId):
    endIndex = (objectId.find("(c") - 1)
    stIndex = 0
    if (objectId.find("\"") == 0):
        stIndex = 1
    return objectId[stIndex:endIndex+1]

print "Starting ..."

node = getName(getNodeId(""))
server = getName(getServerId(""))

print "Creating Custom Path Env Variable ..."

AdminTask.setVariable('[-variableName CUST_PATH -variableValue /work/config/ -scope Cell=DefaultCell01]')
AdminTask.setVariable('[-variableName CUST_PATH -variableValue /work/config/ -scope Node=DefaultNode01]')
AdminTask.setVariable('[-variableName CUST_PATH -variableValue /work/config/ -scope  Node=DefaultNode01,Server=server1]')
AdminConfig.save()

print "Enabling TLS1.2 ..."
AdminTask.listCertStatusForSecurityStandard('[-fipsLevel SP800-131]')
AdminTask.convertCertForSecurityStandard('[-fipsLevel SP800-131]')
AdminTask.enableFips('[-enableFips true -fipsLevel SP800-131]')
print AdminTask.getFipsInfo()
AdminConfig.save()	

print "Installing Postgresql TLS1.2 Certificate..."

AdminTask.addSignerCertificate('[-keyStoreName NodeDefaultTrustStore -keyStoreScope (cell):DefaultCell01:(node):DefaultNode01 -certificateAlias postgres -certificateFilePath ${CUST_PATH}/ibmcloud.cer -base64Encoded true]')
AdminConfig.save()

print "Installing J2C Auth data..."

security = AdminConfig.getid('/Cell:DefaultCell01/Security:/')
alias = ['alias', 'DefaultNode01/postgreAuth']
userid = ['userId', 'ibm_cloud_9b4b8a88_9f9b_4687_a36d_9099038efbae']
password = ['password', 'dae62724fbf067a147103b334b361e6323e006aa75f3647efaed1660314d5ae6']
jaasAttrs = [alias, userid, password]
AdminConfig.create('JAASAuthData', security, jaasAttrs)
AdminConfig.save()

print "Installing JDBC provider..."

AdminJDBC.createJDBCProvider("DefaultNode01", "server1", "PostgreSQL JDBC Provider", "org.postgresql.jdbc2.optional.ConnectionPool", "classpath=${CUST_PATH}/postgresql-9.4-1206-jdbc42.jar, description='PostgreSQL JDBC Provider', providerType='PostgreSQL JDBC Driver Provider'") 
AdminConfig.save()

print "Installing Hello World ..." 

parms = "-appname Application"
parms += " -node " + node + " -server " + server
parms += " -nouseMetaDataFromBinary"
app = AdminApp.install("/work/config/app.ear", [parms])

print "Installing SSMAdmin ..."

parms1 = "-appname SSMAdmin2"
parms1 += " -node " + node + " -server " + server
parms1 += " -nouseMetaDataFromBinary"
AdminApp.install("/work/config/SSMAdmin2.ear", [parms1])

print "Installing SSMServer ..."

parms2 = "-appname SSMServer2"
parms2 += " -node " + node + " -server " + server
parms2 += " -nouseMetaDataFromBinary"
AdminApp.install("/work/config/SSMServer2.ear", [parms2])

print "Installing HostAlias ..."

AdminConfig.create('HostAlias', AdminConfig.getid('/VirtualHost:default_host/'), '[[port "31230"] [hostname "*"]]')
AdminConfig.create('HostAlias', AdminConfig.getid('/VirtualHost:admin_host/'), '[[port "31240"] [hostname "*"]]')
AdminConfig.save()
