'''
translate.py 
Tarik Tosun
2016-03-07
University of Pennsylvania

Translates designs from XML representation (VSPARC) to SmoresDesign objects
for Embedding.
'''


import networkx as nx # graph library
import xml.etree.ElementTree as ET # xml parsing

# Embedding stuff:
from Embedding import SmoresDesign
from Embedding import SmoresModule

# other:
import pdb

class Translator(): 
    '''Translates designs from XML representation (VSPARC) to SmoresDesign objects for Embedding.
    '''
    # dofMap maps the names Jim uses for DoF to the numbers I use.
    # NOTE: Right and left might be flipped, I'm not sure.
    dofMap = {'FrontWheel': 0,
              'BackPlate' : 4,
              'RightWheel': 3,
              'LeftWheel' : 2
              }

    def __init__(self):
        pass


    def translateDesign(self, filename, rootname, root_dof_name):
        ''' Translates design from XML to SmoresDesign. '''
        module_list = []
        self.buildModuleGraph(module_list, filename, rootname, root_dof_name)
        root_module = module_list[0]
        new_design = SmoresDesign.SmoresDesign(root_module, module_list)
        return new_design

    def parseXML(self, filename):
        ''' Parses xml file in filename. '''
        xTree = ET.parse(filename)
        xRoot = xTree.getroot()
        anchorModuleName = xRoot.find('anchorModuleName')
        xModuleStates = xRoot.find('ModuleStates')
        moduleNames = [ms.get('name') for ms in xModuleStates]
        xConnections = xRoot.find('Connections')
        return (moduleNames, xConnections)

    def buildNxGraph(self, filename):
        ''' builds networkx graph, which is used to conveniently root (and re-root) a design before generating
        the Embedding structure. '''
        (moduleNames, xConnections) = self.parseXML(filename)
        G = nx.Graph()
        for name in moduleNames:
            G.add_node(name)
        for connection in xConnections:
            mn1 = connection.find('moduleName1').text
            mn2 = connection.find('moduleName2').text
            dof1 = connection.find('nodeName1').text
            dof2 = connection.find('nodeName2').text
            angle = connection.find('angle').text
            G.add_edge(mn1,mn2)
            G.edge[mn1][mn2][mn1]=dof1
            G.edge[mn1][mn2][mn2]=dof2
            G.edge[mn1][mn2]['angle']=angle
        return G

    def buildModuleGraph(self, moduleList, filename, rootname, root_dof_name):
        ''' Builds module graph (Embedding objects) '''
        G = self.buildNxGraph(filename)
        newModule = self.makeModule(G, rootname, None, root_dof_name)
        moduleList.append( newModule )
        G.node[rootname]['module'] = newModule
        children = nx.bfs_successors(G, rootname)
        self.buildModuleGraphDFS(G, rootname, children, moduleList)

    def buildModuleGraphDFS(self, G, nodeName, children, moduleList):
        ''' Recursive function that traverses nx graph in depth-first fashion. '''
        if not children.has_key(nodeName):
            # this node has no children; return
            return
        for child in children[nodeName]:
            newModule = self.makeModule(G, child, nodeName)
            moduleList.append( newModule )
            G.node[child]['module'] = newModule
            self.buildModuleGraphDFS(G, child, children, moduleList)

    def makeModule(self, G, nodeName, parentName, root_dof_name=None):
        ''' Returns a SmoresModule object created from the nx node. Also links
        the parent to the child appropriately.'''
        if parentName is None:
            # root module case
            newModule = SmoresModule.SmoresModule(nodeName, self.dofMap[root_dof_name])
            return newModule
        else:
            parentEdge = G.edge[parentName][nodeName]
            # check the connection angle.  For now, non-zero angles are not allowed.
            assert parentEdge['angle'] == '0', 'Non-zero connection angles are not allowed.'
            #
            root_node_number = self.dofMap[parentEdge[nodeName]] # the number of the root node of the child module
            child_node_number = self.dofMap[parentEdge[parentName]] # the number of the child node of the parent module.
            newModule = SmoresModule.SmoresModule(nodeName, root_node_number)
            parentModule = G.node[parentName]['module']
            try:
                parentModule.add_child_module(child_node_number, newModule)
            except:
                pdb.set_trace()
            return newModule

    if __name__ == "__main__":
        filename = 'myThing.xml'
        T = EmbeddingTranslator(filename)

