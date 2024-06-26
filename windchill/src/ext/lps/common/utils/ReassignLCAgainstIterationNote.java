package ext.lps.common.utils;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.ptc.core.meta.common.TypeIdentifierHelper;
import com.ptc.core.meta.type.mgmt.server.impl.WTTypeDefinition;
import com.ptc.windchill.suma.part.ManufacturerPart;

import wt.doc.WTDocument;
import wt.enterprise.RevisionControlled;
import wt.epm.EPMDocument;
import wt.fc.Persistable;
import wt.fc.PersistenceHelper;
import wt.fc.QueryResult;
import wt.fc.WTObject;
import wt.fc.collections.WTArrayList;
import wt.inf.container.WTContainerRef;
import wt.lifecycle.LifeCycleHelper;
import wt.method.RemoteAccess;
import wt.method.RemoteMethodServer;
import wt.part.WTPart;
import wt.pds.StatementSpec;
import wt.query.QuerySpec;
import wt.query.SearchCondition;
import wt.session.SessionMgr;
import wt.type.TypedUtilityServiceHelper;
import wt.util.WTAttributeNameIfc;
import wt.vc.Iterated;
import wt.vc.wip.WorkInProgressHelper;

/**
 * This class is a utility for Windchill administrators users.
 * The ReassignLCAgainstIterationNote class is designed to reassign lifecycle templates for various WTDocuments, WTParts, and ManufacturerParts
 * It handles objects filtered by soft type (ex: ext.lps.power.POWERDefinitionDocument) and filtered by a substring of ITERATION_NOTE value.
 * 
 * This utility class supports processing documents, parts, and manufacturer parts, segregating them by their
 * defined types added in lifecycleTemplatesMap (e.g., definition documents, manufacturing documents, standard components, consumable parts,
 * electronic parts, mechanical parts, equipment parts, software parts, tools, test benches, manufacturer parts,
 * and standard reference parts, cad documents, cad drawings).
 * 
 * The lifecycle reassignment process is conditional upon the type of object (document, part, manufacturer part)
 * and ensures that the correct lifecycle template is applied based on the object's soft type. 
 * The class allows for both simulation and execution modes.
 * The class allows for using bulk api (List of objects) or simple api (object level) from Windchill.
 * * 
 * Compile in Windchill Shell:
 * D:\ptc\Windchill_12.1\Windchill> ant -f bin/tools.xml class -Dclass.source=D:\\ptc\\Windchill_12.1\\Windchill\\src\\ext\\lps\\common\\utils -Dclass.includes=ReassignLCAgainstIterationNote.java
 * D:\ptc\Windchill_12.1\Windchill> windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** SIMULATE SIMPLE ext.lps.power.POWERMechanicalStandardPart "Migration-Zeus"
 * D:\ptc\Windchill_12.1\Windchill> windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERMechanicalStandardPart "Migration-Zeus"
 * 
 * Authored by Raphael Leveque
 *
 */
public class ReassignLCAgainstIterationNote implements RemoteAccess {
	
	/** Logger */
	//private static Logger LOG = LogManager.getLogger(ReassignLCAgainstIterationNote.class);
	
	/** Doc Types **/
	private static final String TYPE_DOC_DEF = "ext.lps.power.POWERDefinitionDocument";
	private static final String TYPE_DOC_MANUF = "ext.lps.power.POWERManufacturingDocument";
	private static final String TYPE_DOC_REF = "ext.lps.power.POWERReferenceDocument";
	private static final String TYPE_DOC_STD = "ext.lps.power.POWERStandardComponentDocument";
	/** Part - Standard - Types **/
	private static final String TYPE_PART_STD_CONSUMABLE = "ext.lps.power.POWERConsumableStandardPart";
	private static final String TYPE_PART_STD_ELECTRONIC = "ext.lps.power.POWERElectronicStandardPart";
	private static final String TYPE_PART_STD_MECHANICAL = "ext.lps.power.POWERMechanicalStandardPart";
	private static final String TYPE_PART_STD_GENERIC_MATERIAL = "ext.lps.power.POWERGenericMaterialPart";
	/** Part - Design - Types **/
	private static final String TYPE_PART_ELECTRONIC = "ext.lps.power.POWERElectronicDesignPart";
	private static final String TYPE_PART_MECHANICAL = "ext.lps.power.POWERMechanicalDesignPart";
	private static final String TYPE_PART_EQUIPMENT = "ext.lps.power.POWEREquipmentPart";
	private static final String TYPE_PART_SOFTWARE = "ext.lps.power.POWERSoftwarePart";
	private static final String TYPE_PART_TOOL = "ext.lps.power.POWERToolPart";
	private static final String TYPE_PART_TEST_BENCH = "ext.lps.power.POWERTestBenchPart";
	/** Part - Manufacturer - Types **/
	private static final String TYPE_MANUFACTURER_PART_MANUFACTURER_PART = "ext.lps.power.POWERManufacturerPart";
	private static final String TYPE_MANUFACTURER_PART_STD_REF_PART = "ext.lps.power.POWERStandardReferencePart";
	/** EPMDoc - Types **/
	private static final String TYPE_CAD_CADDocument = "ext.lps.power.POWERCADDocument"; 
	private static final String TYPE_CAD_CADDrawing = "ext.lps.power.POWERCADDrawing";
	private static final String TYPE_CAD_StandardPartCADDocument = "ext.lps.power.POWERStandardPartCADDocument";
	/** DEBUG ONLY - WTPart or WTDocument **/
	private static final String TYPE_PART = "wt.part.WTPart";
	private static final String TYPE_DOCUMENT = "wt.doc.WTDocument";

    // Mapping of types to life cycle templates
	private static final Map<String, String> lifecycleTemplatesMap = new HashMap<>();
    // Mapping from class to its type definition reference and iteration note field
	private static final Map<Class<? extends WTObject>, TypeMappingInfo> classToTypeMapping = new HashMap<>();


    private static void initResources() {
		// Initialize the map with the types and their corresponding life cycle templates
    	// !! Make sure that this array contains all soft types declared above !!
        lifecycleTemplatesMap.put(TYPE_DOC_DEF, "POWER Design Part LifeCycle");
        lifecycleTemplatesMap.put(TYPE_DOC_MANUF, "POWER Design Part LifeCycle");
        lifecycleTemplatesMap.put(TYPE_DOC_REF, "POWER Reference Document Life Cycle");
        lifecycleTemplatesMap.put(TYPE_DOC_STD, "POWER Standard Component Document Life Cycle");
        lifecycleTemplatesMap.put(TYPE_PART_STD_CONSUMABLE, "POWER Standard Part Life Cycle");
        lifecycleTemplatesMap.put(TYPE_PART_STD_ELECTRONIC, "POWER Standard Part Life Cycle");
        lifecycleTemplatesMap.put(TYPE_PART_STD_MECHANICAL, "POWER Standard Part Life Cycle");
        lifecycleTemplatesMap.put(TYPE_PART_STD_GENERIC_MATERIAL, "POWER Generic Material Part Life Cycle");
        lifecycleTemplatesMap.put(TYPE_PART_ELECTRONIC, "POWER Design Part LifeCycle");
        lifecycleTemplatesMap.put(TYPE_PART_MECHANICAL, "POWER Design Part LifeCycle");
        lifecycleTemplatesMap.put(TYPE_PART_EQUIPMENT, "POWER Design Part LifeCycle");
        lifecycleTemplatesMap.put(TYPE_PART_SOFTWARE, "POWER Design Part LifeCycle");
        lifecycleTemplatesMap.put(TYPE_PART_TOOL, "POWER Design Part LifeCycle");
        lifecycleTemplatesMap.put(TYPE_PART_TEST_BENCH, "POWER Design Part LifeCycle"); // Not used Mig1
        lifecycleTemplatesMap.put(TYPE_MANUFACTURER_PART_MANUFACTURER_PART, "POWER Manufacturer Part Life Cycle");
        lifecycleTemplatesMap.put(TYPE_MANUFACTURER_PART_STD_REF_PART, "POWER Standard Reference Part Life Cycle");
        lifecycleTemplatesMap.put(TYPE_CAD_CADDocument, "POWER Design Part LifeCycle");
        lifecycleTemplatesMap.put(TYPE_CAD_CADDrawing, "POWER Design Part LifeCycle");
        lifecycleTemplatesMap.put(TYPE_CAD_StandardPartCADDocument, "POWER Standard CAD Document Part Life Cycle");
		/** DEBUG ONLY - WTPart or WTDocument **/
        lifecycleTemplatesMap.put(TYPE_PART, "BasicTestForReassign");
        lifecycleTemplatesMap.put(TYPE_DOCUMENT, "BasicTestForReassign");
        
		// Populate the map with class-specific information
        classToTypeMapping.put(WTDocument.class, new TypeMappingInfo(WTDocument.TYPE_DEFINITION_REFERENCE + "." + WTAttributeNameIfc.REF_OBJECT_ID, WTDocument.ITERATION_NOTE));
        classToTypeMapping.put(WTPart.class, new TypeMappingInfo(WTPart.TYPE_DEFINITION_REFERENCE + "." + WTAttributeNameIfc.REF_OBJECT_ID, WTPart.ITERATION_NOTE));
        classToTypeMapping.put(ManufacturerPart.class, new TypeMappingInfo(ManufacturerPart.TYPE_DEFINITION_REFERENCE + "." + WTAttributeNameIfc.REF_OBJECT_ID, ManufacturerPart.ITERATION_NOTE));
        classToTypeMapping.put(EPMDocument.class, new TypeMappingInfo(EPMDocument.TYPE_DEFINITION_REFERENCE + "." + WTAttributeNameIfc.REF_OBJECT_ID, EPMDocument.ITERATION_NOTE));

    }
    
    private static class TypeMappingInfo {
        String typeDefinitionReference;
        String iterationNoteField;

        public TypeMappingInfo(String typeDefinitionReference, String iterationNoteField) {
            this.typeDefinitionReference = typeDefinitionReference;
            this.iterationNoteField = iterationNoteField;
        }
    }
    // Private method to get the life cycle template
    private static String getLifeCycleTemplateName(String type) {
        return lifecycleTemplatesMap.getOrDefault(type, "Unknown Type");
    }

	/**
	 * 
	 * @return all latest version/iteration of a WTObject with filtering on type Definition and iteration Note
	 * @throws Throwable
	 */
    private static List<? extends RevisionControlled> getLatestObjects(Class<? extends RevisionControlled> clazz, String softType, String iterationNote) throws Throwable {
        List<RevisionControlled> listObjects = new ArrayList<>();

        QuerySpec query = new QuerySpec();

        int idxObject = query.addClassList(clazz, true);
        int idxTypeDef = query.appendClassList(WTTypeDefinition.class, false);

        // Retrieve class-specific mapping info
        TypeMappingInfo mappingInfo = classToTypeMapping.get(clazz);

        // search soft type given its short name
        query.appendWhere(new SearchCondition(WTTypeDefinition.class, WTTypeDefinition.NAME, SearchCondition.EQUAL, softType), new int[]{idxTypeDef});
        query.appendAnd();
        query.appendWhere(new SearchCondition(WTTypeDefinition.class, WTAttributeNameIfc.ID_NAME, clazz, mappingInfo.typeDefinitionReference), new int[]{idxTypeDef, idxObject});

        // select only latest iteration
        query.appendAnd();
        query.appendWhere(new SearchCondition(clazz, Iterated.LATEST_ITERATION, SearchCondition.IS_TRUE), new int[]{idxObject});

        // select by given iteration note
        query.appendAnd();
        //query.appendWhere(new SearchCondition(clazz, mappingInfo.iterationNoteField, SearchCondition.LIKE, iterationNote), new int[]{idxObject});
        query.appendWhere(new SearchCondition(clazz, mappingInfo.iterationNoteField, SearchCondition.LIKE, "%" + iterationNote + "%"), new int[]{idxObject});

		/** DEBUG ONLY **/
        //System.out.println("ReassignLCAgainstIterationNote -- INFO -- Query for " + clazz.getSimpleName() + ": " + query.toString());

        QueryResult qsResult = PersistenceHelper.manager.find((StatementSpec) query);
        if (qsResult != null) {
            while (qsResult.hasMoreElements()) {
                Object element = qsResult.nextElement();
                // Check if the element is actually an array, as expected
                if (element instanceof Persistable[]) {
                    Persistable[] persistables = (Persistable[]) element;
                    // Check if the first element of the array is an instance of RevisionControlled
                    if (persistables.length > 0 && persistables[0] instanceof RevisionControlled) {
                        RevisionControlled controlledObject = (RevisionControlled) persistables[0];
                        listObjects.add(controlledObject);
                    } else {
                        // Handle the case where it's not the expected type
                    	System.out.println("ReassignLCAgainstIterationNote -- ERROR : Unexpected object type: " + (persistables.length > 0 ? persistables[0].getClass().getName() : "empty array"));
                    }
                } else {
                    // Handle the case where the query result is not an array as expected
                	System.out.println("ReassignLCAgainstIterationNote -- ERROR : Query result element is not of type Persistable[]: " + element.getClass().getName());
                }
            }
        }

        return listObjects;
    }
    
	/**
	 * 
	 * @param object
	 * @return Container of object
	 * @throws Exception
	 */
	private static WTContainerRef getContainerRef(RevisionControlled object) throws Exception {
		
		WTContainerRef containerRef = null;
		// Return container reference from class-specific information
		if ( object instanceof WTPart ) {
			containerRef = ((WTPart) object).getContainerReference();
		} else if ( object instanceof WTDocument ) {
			containerRef = ((WTDocument) object).getContainerReference();
		} else if ( object instanceof ManufacturerPart ) {
			containerRef = ((ManufacturerPart) object).getContainerReference();
		} else if ( object instanceof EPMDocument ) {
			containerRef = ((EPMDocument) object).getContainerReference();
		} else {
			throw new Exception("The class type " + object.getClass().toString() + " is not accepted");
		}
		
		return containerRef;
	}
	
	/**
	 * 
	 * @param object
	 * @return number of object
	 * @throws Exception
	 */
	private static String getNumber(RevisionControlled object) throws Exception {
		
		String number = null;
		// Return number from class-specific information
		if ( object instanceof WTPart ) {
			number = ((WTPart) object).getNumber();
		} else if ( object instanceof WTDocument ) {
			number = ((WTDocument) object).getNumber();
		} else if ( object instanceof ManufacturerPart ) {
			number = ((ManufacturerPart) object).getNumber();
		} else if ( object instanceof EPMDocument ) {
			number = ((EPMDocument) object).getNumber();
		} else {
			throw new Exception("The class type " + object.getClass().toString() + " is not accepted");
		}
		
		return number;
	}

    /**
     * Reassigns lifecycle state of provided WTObjects based on the simulation mode and bulk operation mode.
     *
     * @param isSimulation Indicates if the operation should be simulated (true) or executed (false).
     * @param objects Either a single RevisionControlled object or a list of RevisionControlled objects.
     * @param targetLCTemplateName The target life cycle template name for reassignment.
     * @param bulk Indicates if the operation should be processed using bulk windchill api.
     * @throws Exception Throws an exception if an error occurs during processing.
     */
    private static void reassignLC(List<? extends RevisionControlled> objects, Boolean isSimulation, Boolean isBulk, String targetLCTemplateName) throws Exception {
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- Execute reassignLC with <SIMULATE(TRUE) or RUN(FALSE)> "+ isSimulation.toString()+" with <BULK(TRUE) or SIMPLE(FALSE)> "+ isBulk.toString()+" and <targetLCTemplateName> "+targetLCTemplateName);
        WTArrayList wtListBulk = new WTArrayList();
        for (RevisionControlled object : objects) {
            String currentState = object.getLifeCycleState().toString();
            String currentLCTemplateName = object.getLifeCycleTemplate().getName();
            String iterationInfo = object.getIterationDisplayIdentifier().toString();
    		String objectNumber = getNumber(object);
    		String localizedTypeName = TypedUtilityServiceHelper.service.getLocalizedTypeName(TypeIdentifierHelper.getType(object), null);
    		String classType = object.getClass().getSimpleName();
			WTContainerRef containerRef = getContainerRef(object);
   		
            if (targetLCTemplateName.equals(currentLCTemplateName)) {
                System.out.println("ReassignLCAgainstIterationNote -- INFO -- SKIPPED - LC Template ("+targetLCTemplateName+") already set for " + classType + " ; " + localizedTypeName + " ; " + objectNumber + " ; " + iterationInfo + " ; " + currentLCTemplateName + " ; " + currentState);
                continue;
            }
            if (WorkInProgressHelper.isCheckedOut(object)) {
            	System.out.println("ReassignLCAgainstIterationNote -- ERROR -- CHECKED-OUT for " + classType + " ; " + localizedTypeName + " ; " + objectNumber + " ; " + iterationInfo + " ; " + currentLCTemplateName + " ; " + currentState);
				continue;
            }
            if (isSimulation != null && isSimulation) {
                System.out.println("ReassignLCAgainstIterationNote -- INFO -- Simulation mode: Re-assign would be processed here for " + classType + " ; " + localizedTypeName + " ; " + objectNumber + " ; " + iterationInfo + " ; State: " + currentState + " ; Current template: " + currentLCTemplateName + " ; New template: " + targetLCTemplateName + " -- Relaunch with \"RUN\" option to process Re-assign");
				
            } else {
                wtListBulk.add(object); // Add eligible objects to the list for reassignment in case of bulk
                if (!isBulk) {
    				// Reassign	unique object in case of not bulk
                	WTArrayList uniqueObjectList = new WTArrayList();
                	uniqueObjectList.add(object);
					LifeCycleHelper.service.reassign(uniqueObjectList, LifeCycleHelper.service.getLifeCycleTemplateReference(targetLCTemplateName), containerRef, object.getLifeCycleState());
					object = (RevisionControlled) PersistenceHelper.manager.refresh(object);
			        System.out.println("ReassignLCAgainstIterationNote -- INFO -- LC Template has been RE-ASSSIGNED for " + classType + " ; " + localizedTypeName + " ; " + objectNumber + " ; " + iterationInfo + " ; State: " + currentState + " ; Current template: " + currentLCTemplateName + " to new template " + targetLCTemplateName);
			        //// object.getIdentifier()
                }
            }
        }

        if ( !isSimulation && wtListBulk.size() > 0 && isBulk) {
            // Perform the bulk reassignment
            LifeCycleHelper.service.reassign(
            		wtListBulk, 
            		LifeCycleHelper.service.getLifeCycleTemplateReference(targetLCTemplateName) /* target lifecycle template */, 
            		null /* container ref can be null - not needed for this api  */, 
            		null /* keep same state */);
            System.out.println("ReassignLCAgainstIterationNote -- INFO -- Bulk reassignment completed for " + wtListBulk.size() + " objects.");
        }
    }


	/**
	 * Launch reassign with proper query depending on soft type
	 * @param isSimulation
	 * @param targetLCTemplateName
	 * @throws Throwable
	 */
   public static void processReassign(Boolean isSimulation, Boolean isBulk, String softType, String iterationNote) throws Throwable {
		try {
			initResources();
			// Validate softType
			List<String> validTypes = Arrays.asList(
				TYPE_DOC_DEF, TYPE_DOC_MANUF, TYPE_DOC_REF, TYPE_DOC_STD, 
				TYPE_PART_STD_CONSUMABLE, TYPE_PART_STD_ELECTRONIC, TYPE_PART_STD_MECHANICAL, TYPE_PART_STD_GENERIC_MATERIAL,
				TYPE_PART_ELECTRONIC, TYPE_PART_MECHANICAL, TYPE_PART_EQUIPMENT, TYPE_PART_SOFTWARE, TYPE_PART_TOOL, TYPE_PART_TEST_BENCH, 
				TYPE_MANUFACTURER_PART_MANUFACTURER_PART, TYPE_MANUFACTURER_PART_STD_REF_PART,
				TYPE_CAD_CADDocument, TYPE_CAD_CADDrawing, TYPE_CAD_StandardPartCADDocument,
				TYPE_PART, TYPE_DOCUMENT);

			if (!validTypes.contains(softType)) {
				System.out.println("ReassignLCAgainstIterationNote -- ERROR -- main_reassignLC: Unknown softType: lifecycleTemplatesMap array does not contain this type " + softType);
				return;
			}

			// Get the life cycle template name based on the softType
			String lifecycleTemplateName = getLifeCycleTemplateName(softType);

			// Determine the processing action based on softType's category calculated from its value
			if (softType.contains("CADDocument") || softType.contains("CADDrawing")) {
				// Process as EPMDocument
				System.out.println("ReassignLCAgainstIterationNote -- INFO -- processReassign: get Latest EPMDocs on <" + softType + "> with iteration note <" + iterationNote +">");
				reassignLC(getLatestObjects(EPMDocument.class, softType, iterationNote), 
						isSimulation, isBulk, 
						lifecycleTemplateName);
			} else if (softType.contains("ManufacturerPart") || softType.contains("StandardReferencePart")) {
				// Process as ManufacturerPart
				System.out.println("ReassignLCAgainstIterationNote -- INFO -- processReassign: get Latest Manuf Parts on <" + softType + "> with iteration note <" + iterationNote +">");
				reassignLC(getLatestObjects(ManufacturerPart.class, softType, iterationNote), 
						isSimulation, isBulk, 
						lifecycleTemplateName);
			} else if (softType.contains("Document")) {
				// Process as WTDocument
				System.out.println("ReassignLCAgainstIterationNote -- INFO -- processReassign: get Latest WTDocs on <" + softType + "> with iteration note <" + iterationNote +">");
				reassignLC(getLatestObjects(WTDocument.class, softType, iterationNote), 
						isSimulation, isBulk,
						lifecycleTemplateName);
			} else if (softType.contains("Part")) {
				// Process as WTPart
				System.out.println("ReassignLCAgainstIterationNote -- INFO -- processReassign: get Latest WTParts on <" + softType + "> with iteration note <" + iterationNote +">");
				reassignLC(getLatestObjects(WTPart.class, softType, iterationNote), 
						isSimulation, isBulk, 
						lifecycleTemplateName);
			}  else {
				System.out.println("ReassignLCAgainstIterationNote -- ERROR -- processReassign: no action available for soft type " + softType);
				return;
			}
		} catch (Throwable th) {
	        System.out.println("ReassignLCAgainstIterationNote -- ERROR -- processReassign:" + th.getMessage());
	        th.printStackTrace();
		}
    }

	/**
	 * Main method
	 * 
	 * @param args
	 */
	public static void main(String[] args) {

		try {
			
			// Arguments
			if (args == null || (args.length!=6)) {
				printUsage();
	            System.exit(1);           	  
			} else {
				// Invoke export command
				RemoteMethodServer rms = RemoteMethodServer.getDefault();
				// Administrator account
				rms.setUserName(args[0]);
				// Administrator password
				rms.setPassword(args[1]);
				// Simulation/Run mode
				Boolean isSimulation = Boolean.TRUE;
				if ("RUN".equals(args[2])) {

					isSimulation = Boolean.FALSE;
				}	
				// Bulk/Simple mode
				Boolean isBulk = Boolean.FALSE;
				if ("BULK".equals(args[3])) {
					isBulk = Boolean.TRUE;
				}	
				// Soft Type filtering
				String softType = args[4];			
				// Iteration Note filtering
				String iterationNote = args[5];		
				// Invocation
				Class<?> aClass[] = { Boolean.class, Boolean.class, String.class, String.class};
				Object argsObj[] = { isSimulation, isBulk, softType, iterationNote };
				SessionMgr.getPrincipal();
		        System.out.println("ReassignLCAgainstIterationNote -- INFO -- Execution of ReassignLCAgainstIterationNote with <admin_login> "+args[0]+" <SIMULATE (true) or RUN (false)> "+isSimulation.toString()+" <BULK (true) or SIMPLE (false)> "+isBulk.toString()+" <soft_type> "+softType+" <iteration_note> "+iterationNote);
				System.out.println("ReassignLCAgainstIterationNote -- INFO -- See MethodServer log");
				rms.invoke("processReassign", ReassignLCAgainstIterationNote.class.getName(), null, aClass, argsObj);
				System.exit(0);
			}
				
		} catch (Throwable th) {
	        System.out.println("ReassignLCAgainstIterationNote -- ERROR : "+ th.getMessage());
	    	th.printStackTrace();
			System.exit(1);
		}
	}
	
    /**
     * Displays usage of this tool (command) when it's launched from command line
     * 
     **/
    private static void printUsage() {
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- Usage: ReassignLCAgainstIterationNote <admin_login> <password> <simulate_or_run> <bulk_or_simple> <soft_type> <iteration_note>");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- Designed to reassign lifecycle templates for various WTDocuments, WTParts, EPMDocuments and ManufacturerParts."); 
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- It handles objects filtered by soft type (ex: ext.lps.power.POWERDefinitionDocument) and filtered by a substring of ITERATION_NOTE value.");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- It ensures that the correct lifecycle template is applied based on the object's soft type.");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- It allows for both simulation and execution modes.");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- It allows for using either bulk api (List of objects) or simple api (object level) from Windchill.");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- Arg 1 = login with admin rights");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- Arg 2 = password");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- Arg 3 = Can be SIMULATE or RUN");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- Arg 4 = Can be BULK or SIMPLE");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- Arg 5 = soft type criteria (ex: ext.lps.power.POWERDefinitionDocument)");	         
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- Arg 6 = ITERATION_NOTE criteria (ex: Migration-Zeus or Migration-Agile or Migration-Future)");	 
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- Example of command using SIMULATE mode (simulate LC reassignment without any change and showing in method server log impacted objects):");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** SIMULATE BULK ext.lps.power.POWERMechanicalStandardPart \"Migration-Zeus" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- Examples of command using RUN mode (execute LC reassignment in database):");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERDefinitionDocument \"Migration-Agile" + "\"");	
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERManufacturingDocument \"Migration-Agile" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERReferenceDocument \"Migration-Agile" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERStandardComponentDocument \"Migration-Zeus" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERConsumableStandardPart \"Migration-Zeus" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERElectronicStandardPart \"Migration-Zeus" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERMechanicalStandardPart \"Migration-Zeus" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERGenericMaterialPart \"Migration-Agile" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERElectronicDesignPart \"Migration-Agile" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERMechanicalDesignPart \"Migration-Agile" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWEREquipmentPart \"Migration-Agile" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERSoftwarePart \"Migration-Agile" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERToolPart \"Migration-Agile" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERTestBenchPart \"Migration-Agile" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERManufacturerPart \"Migration-Zeus" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERStandardReferencePart \"Migration-Zeus" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERCADDocument \"Migration-Future" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERCADDrawing \"Migration-Future" + "\"");
        System.out.println("ReassignLCAgainstIterationNote -- INFO -- windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERStandardPartCADDocument \"Migration-Future" + "\"");
    }

}
