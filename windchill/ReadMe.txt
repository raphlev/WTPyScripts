This package installs windchill configuration needed for Zeus Test Migration RUN 1.
It contains also configuration for Agile, but the specific config file for Agile are not loaded into Windchill by the loader

-----------------------------------------------------------------------------------------------------------------

Instructions:
1. unzip the content in $WT_HOME
2. open windchill shell as Administrator
3. launch following command: LoadFileSet_SEP_BEFORE_Migration_ZEUS.bat
   . Make sure Java build is successful
   . Enter Y/N to restart Windchill (restart needed if new version of Java class is provided)
-----------------------------------------------------------------------------------------------------------------

Content of load files:

Java class to launch LC Reassignment (see commen in Java class for details how to use it)
- src\ext\lps\common\utils\ReassignLCAgainstIterationNote.java
 * This class is a utility for Windchill administrators users.
 * The ReassignLCAgainstIterationNote class is designed to reassign lifecycle templates for various WTDocuments, WTParts, and ManufacturerParts
 * It handles objects filtered by their soft type and an iteration note.
 * 
 * This utility class supports processing documents, parts, and manufacturer parts, segregating them by their
 * defined types (e.g., definition documents, manufacturing documents, standard components, consumable parts,
 * electronic parts, mechanical parts, equipment parts, software parts, tools, test benches, manufacturer parts,
 * and standard reference parts).
 * 
 * The lifecycle reassignment process is conditional upon the type of object (document, part, manufacturer part)
 * and ensures that the correct lifecycle template is applied based on the object's soft type. 
 * The class allows for both simulation and execution modes.
 * The class allows for using bulk api (List of objects) or simple api (object level) from Windchill.

Agile - New Products (Spec Agile_WNC_Containers_for_Migration.xlsx)
- products "POWER Program Product Template" required for Agile migration (subject to change, TBC when to load them into PPROD/PROD)
- POWERNewAgileProductLoader.xml
- POWERNewAgileProductAssignViewerRole.xml

Zeus - New Suppliers (Specs Calculate_New_Manufacturers.xlsx - Calculate_New_StandardAuthority.xlsx)
- suppliers "Manufacturer" and "StandardAuthority" needed for Zeus migration (subject to change, TBC when to load them into PPROD/PROD)
- ext/migration/suppliers_for_zeus/LoadOrganizations_For_Migration_Manufacturers.xml
- ext/migration/suppliers_for_zeus/LoadManufacturers_For_Migration_Manufacturers.xml
- ext/migration/suppliers_for_zeus/LoadOrganizations_For_Migration_StandardAuthority.xml
- ext/migration/suppliers_for_zeus/LoadManufacturers_For_Migration_StandardAuthority.xml

Agile & Zeus - Versioning
- LoadSeries.xml
- new Legacy values for NumericStateBased
- "-" and "A" - Test Migration Run 1 "-" is needed for Agile, and "A" will be needed for Zeus
- "S" is needed to fix loading issue on Agile server - value already used in Agile DB after rehosting from PROD in March, this issue was not encountered on Zeus rehosted from PROD few weeks before
		
Agile & Zeus - Global Enumerations
- POWERDesignSites.xml : add Chatou and update Reau display name to Créteil
- POWERProductLines.xml : add missing Agile values as Selectable = True (Spec Mapping_SEP_V11_Agile_TestMig1)
- POWERTypeArticleMechanical.xml : add missing Agile values as Selectable = True (Spec Mapping_SEP_V11_Agile_TestMig1
- POWERTypeArticleTool.xml : add missing Agile values as Selectable = True (Spec Mapping_SEP_V11_Agile_TestMig1)

Zeus - Lifecycles
- ext/migration/lifecycles_for_agile_zeus/POWERStandardComponentDocumentForMigrationLifeCycle.xml
- add missing transition for Zeus migration
- needed for Zeus at migration post step for ReassignLC related to POWERStandardComponentDocument
- do not merge in SEP config

Zeus - OIRs
- ext/migration/oirs/POWERStandardComponentDocumentOIR_For_Migration.xml
- add missing transition for Zeus migration
- needed for Zeus at migration post step for ReassignLC related to POWERStandardComponentDocument
- do not merge in SEP config

Agile & Zeus - Reports QueryBuilder
- new reports with criteria (attributes Windchill OOTB/IBAs) which are used for the mapping for Zeus or Agile migration
- additional select criteria IterationNote in order to quey migrated data using %Migration-Zeus% or %Migration-Agile% values (values should be entered by user when using the reports)
- 3 reports available for each sub-type of migrated parts: simple report without link, report with manufacturer parts links, and report with docs links
- 1 report available for manufactuer parts, std Ref parts and documents subtypes

- ext/migration/reports_for_agile_zeus/POWER_Electronic_Standard_Parts_For_Migration_Reports.xml  -- Zeus
- ext/migration/reports_for_agile_zeus/POWER_Mechanical_Standard_Parts_For_Migration_Reports.xml  -- Zeus
- ext/migration/reports_for_agile_zeus/POWER_Consumable_Standard_Parts_For_Migration_Reports.xml  -- Zeus
- ext/migration/reports_for_agile_zeus/POWER_Generic_Material_Parts_For_Migration_Reports.xml  -- Zeus

- ext/migration/reports_for_agile_zeus/POWER_Electronic_Standard_Parts_With_Manufacturer_Parts_For_Migration_Reports.xml  -- Zeus
- ext/migration/reports_for_agile_zeus/POWER_Mechanical_Standard_Parts_With_Manufacturer_Parts_For_Migration_Reports.xml  -- Zeus
- ext/migration/reports_for_agile_zeus/POWER_Consumable_Standard_Parts_With_Manufacturer_Parts_For_Migration_Reports.xml  -- Zeus
- ext/migration/reports_for_agile_zeus/POWER_Generic_Material_Parts_With_Manufacturer_Parts_For_Migration_Reports.xml  -- Zeus
		
- ext/migration/reports_for_agile_zeus/POWER_Electronic_Standard_Parts_With_Documents_For_Migration_Reports.xml  -- Zeus
- ext/migration/reports_for_agile_zeus/POWER_Mechanical_Standard_Parts_With_Documents_For_Migration_Reports.xml  -- Zeus
- ext/migration/reports_for_agile_zeus/POWER_Consumable_Standard_Parts_With_Documents_For_Migration_Reports.xml  -- Zeus
- ext/migration/reports_for_agile_zeus/POWER_Generic_Material_Parts_With_Documents_For_Migration_Reports.xml  -- Zeus

- ext/migration/reports_for_agile_zeus/POWER_Standard_Component_Documents_For_Migration_Reports.xml  -- Zeus
- ext/migration/reports_for_agile_zeus/POWER_Reference_Document_For_Migration_Reports.xml  -- Agile
- ext/migration/reports_for_agile_zeus/POWER_Manufacturing_Document_For_Migration_Reports.xml  -- Agile
- ext/migration/reports_for_agile_zeus/POWER_Definition_Document_For_Migration_Reports.xml  -- Agile

- ext/migration/reports_for_agile_zeus/POWER_Manufacturer_Part_For_Migration_Reports.xml  -- Agile & Zeus
- ext/migration/reports_for_agile_zeus/POWER_Manufacturer_Part_With_Documents_For_Migration_Reports.xml  -- Agile & Zeus
- ext/migration/reports_for_agile_zeus/POWER_Standard_Reference_Part_For_Migration_Reports.xml  -- Agile & Zeus
- ext/migration/reports_for_agile_zeus/POWER_Standard_Reference_Part_With_Documents_For_Migration_Reports.xml  -- Agile & Zeus

- ext/migration/reports_for_agile_zeus/POWER_Electronic_Design_Parts_For_Migration_Reports.xml  -- Agile
- ext/migration/reports_for_agile_zeus/POWER_Mechanical_Design_Parts_For_Migration_Reports.xml  -- Agile
- ext/migration/reports_for_agile_zeus/POWER_Software_Parts_For_Migration_Reports.xml  -- Agile
- ext/migration/reports_for_agile_zeus/POWER_Tool_Parts_For_Migration_Reports.xml  -- Agile
- ext/migration/reports_for_agile_zeus/POWER_Equipment_Parts_For_Migration_Reports.xml  -- Agile
- ext/migration/reports_for_agile_zeus/POWER_Electronic_Design_Parts_With_Manufacturer_Parts_For_Migration_Reports.xml  -- Agile
- ext/migration/reports_for_agile_zeus/POWER_Mechanical_Design_Parts_With_Manufacturer_Parts_For_Migration_Reports.xml  -- Agile
- ext/migration/reports_for_agile_zeus/POWER_Software_Parts_With_Manufacturer_Parts_For_Migration_Reports.xml  -- Agile
- ext/migration/reports_for_agile_zeus/POWER_Tool_Parts_With_Manufacturer_Parts_For_Migration_Reports.xml  -- Agile
- ext/migration/reports_for_agile_zeus/POWER_Equipment_Parts_With_Manufacturer_Parts_For_Migration_Reports.xml  -- Agile	
