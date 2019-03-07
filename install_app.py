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

print "Installing application ..."

node = getName(getNodeId(""))
server = getName(getServerId(""))

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

print "Creating Custom Path Env Variable ..."
AdminTask.setVariable('[-variableName CUST_PATH -variableValue /work/config/ -scope Cell=DefaultCell01]')
AdminTask.showVariables ('[ -scope Cell=DefaultCell01 -variableName CUST_PATH ]')
AdminConfig.save()

print "Installing HostAlias ..."
AdminConfig.create('HostAlias', AdminConfig.getid('/VirtualHost:default_host/'), '[[port "31230"] [hostname "*"]]')
AdminConfig.create('HostAlias', AdminConfig.getid('/VirtualHost:admin_host/'), '[[port "31240"] [hostname "*"]]')
AdminConfig.save()
