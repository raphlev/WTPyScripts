<qml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" bypassAccessControl="false" caseInsensitive="false" addTimeToDateFields="false" mainType="Sourcing Relationship" joinModel="false" xsi:noNamespaceSchemaLocation="qml.xsd"><query><selectOrConstrain distinct="false" group="false"><reportAttribute heading="Manufacturer Part Number" reportAttributeId="Manufacturer_Part_Number" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="Manufacturer Part" isExternal="false" type="java.lang.String" propertyName="number">master&gt;number</column></reportAttribute><reportAttribute heading="Manufacturer Part State" reportAttributeId="Manufacturer_Part_State" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="Manufacturer Part" isExternal="false" type="wt.lifecycle.State" propertyName="lifeCycleState">state.state</column></reportAttribute><reportAttribute heading="Manufacturer Part Name" reportAttributeId="Manufacturer_Part_Name" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="Manufacturer Part" isExternal="false" type="java.lang.String" propertyName="name">master&gt;name</column></reportAttribute><reportAttribute heading="Manufacturer Part Revision" reportAttributeId="Manufacturer_Part_Revision" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="Manufacturer Part" isExternal="false" type="java.lang.String" propertyName="versionInfo.identifier.versionId">versionInfo.identifier.versionId</column></reportAttribute><reportAttribute heading="Manufacturer Name" reportAttributeId="Manufacturer_Name" userCanSelect="true" userCanConstrain="false" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><object alias="Sourcing Relationship" propertyName="manufacturerObj.name"/></reportAttribute><reportAttribute heading="Manufacturer Part Sourcing Status" reportAttributeId="Manufacturer_Part_Sourcing_Status_amlPreference_" userCanSelect="true" userCanConstrain="false" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><object alias="Sourcing Relationship" propertyName="amlPreference"/></reportAttribute><reportAttribute heading="Manufacturer Part Sourcing Order" reportAttributeId="Sourcing_Order" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="Sourcing Relationship" isExternal="false" type="java.lang.Long" propertyName="WCTYPE|com.ptc.windchill.suma.axl.AXLEntry~IBA|POWERSourcingOrder">WCTYPE|com.ptc.windchill.suma.axl.AXLEntry~IBA|POWERSourcingOrder</column></reportAttribute><reportAttribute heading="Part Classification" reportAttributeId="Classification" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="java.lang.String" propertyName="WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|Classification">WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|Classification</column></reportAttribute><reportAttribute heading="Part Number" reportAttributeId="Equipment_Part_Number" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="java.lang.String" propertyName="number">master&gt;number</column></reportAttribute><reportAttribute heading="Part Name" reportAttributeId="Equipment_Part_Name" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="java.lang.String" propertyName="name">master&gt;name</column></reportAttribute><reportAttribute heading="Part State" reportAttributeId="Equipment_Part_State" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="wt.lifecycle.State" propertyName="lifeCycleState">state.state</column></reportAttribute><reportAttribute heading="Part Revision" reportAttributeId="Equipment_Part_Revision" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="java.lang.String" propertyName="versionInfo.identifier.versionId">versionInfo.identifier.versionId</column></reportAttribute><reportAttribute heading="Part Created" reportAttributeId="Created" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="java.sql.Timestamp" propertyName="createTimestamp">thePersistInfo.createStamp</column></reportAttribute><reportAttribute heading="Part Modified" reportAttributeId="Last_Modified" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="java.sql.Timestamp" propertyName="modifyTimestamp">thePersistInfo.modifyStamp</column></reportAttribute><reportAttribute heading="Classification" reportAttributeId="Classification_1" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="java.lang.String" propertyName="WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|Classification">WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|Classification</column></reportAttribute><reportAttribute heading="Part Aircraft" reportAttributeId="Aircraft_1" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="java.lang.String" propertyName="WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|POWERAircraft">WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|POWERAircraft</column></reportAttribute><reportAttribute heading="Part Amendment" reportAttributeId="Amendment" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="java.lang.String" propertyName="WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|POWERAmendment">WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|POWERAmendment</column></reportAttribute><reportAttribute heading="Part BT Substances" reportAttributeId="BT_Substances" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="java.lang.String" propertyName="WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|POWERBTSubstance">WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|POWERBTSubstance</column></reportAttribute><reportAttribute heading="Part Design Site" reportAttributeId="Design_Site" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="java.lang.String" propertyName="WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|POWERDesignSiteForWorkItem">WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|POWERDesignSiteForWorkItem</column></reportAttribute><reportAttribute heading="Part Manufacturing Site" reportAttributeId="Manufacturing_Site" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="java.lang.String" propertyName="WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|POWERManufacturingSite">WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|POWERManufacturingSite</column></reportAttribute><reportAttribute heading="Part Name in english" reportAttributeId="Name_in_english_1" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="java.lang.String" propertyName="WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|POWEREnglishName">WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|POWEREnglishName</column></reportAttribute><reportAttribute heading="Part Product Line" reportAttributeId="Product_Line" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="java.lang.String" propertyName="WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|POWERProductLine">WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart~IBA|POWERProductLine</column></reportAttribute><reportAttribute heading="Part Iteration Note" reportAttributeId="Iteration_Note_1" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Equipment Part" isExternal="false" type="java.lang.String" propertyName="iterationNote">iterationInfo.note</column></reportAttribute></selectOrConstrain><from><table alias="Sourcing Relationship" isExternal="false" xposition="0px" yposition="0px">com.ptc.windchill.suma.axl.AXLEntry</table><table alias="Manufacturer Part" isExternal="false" xposition="555px" yposition="197px">com.ptc.windchill.suma.part.ManufacturerPart</table><table alias="Manufacturer Part Master" isExternal="false" xposition="441px" yposition="0px">com.ptc.windchill.suma.part.ManufacturerPartMaster</table><table alias="POWER Equipment Part" isExternal="false" xposition="24px" yposition="203px">WCTYPE|wt.part.WTPart|ext.lps.LPSPart|ext.lps.power.POWERPart|ext.lps.power.POWEREquipmentPart</table></from><where><compositeCondition type="and"><condition><standardCondition><operand><column alias="POWER Equipment Part" isExternal="false" type="boolean" propertyName="latestIteration">iterationInfo.latest</column></operand><operator type="equal"/><operand><constant type="boolean" isMacro="false" xml:space="preserve">1</constant></operand></standardCondition></condition><condition><standardCondition><operand><column alias="Manufacturer Part" isExternal="false" type="boolean" propertyName="latestIteration">iterationInfo.latest</column></operand><operator type="equal"/><operand><constant type="boolean" isMacro="false" xml:space="preserve">1</constant></operand></standardCondition></condition><condition><standardCondition><operand><column alias="POWER Equipment Part" isExternal="false" type="java.lang.String" propertyName="iterationNote">iterationInfo.note</column></operand><operator type="like"/><operand><constant type="java.lang.String" isMacro="false" xml:space="preserve">%</constant></operand></standardCondition></condition></compositeCondition></where><orderBy><orderByItem type="asc"><reportAttributeReference id="Equipment_Part_Number"/></orderByItem></orderBy><linkJoin><join name="com.ptc.windchill.suma.axl.ManufacturerPartMasterAXLEntry"><fromAliasTarget alias="Manufacturer Part Master"/><toAliasTarget alias="Sourcing Relationship"/></join></linkJoin><referenceJoin><join name="oemPartReference"><fromAliasTarget alias="Sourcing Relationship"/><toAliasTarget alias="POWER Equipment Part"/></join><join name="masterReference"><fromAliasTarget alias="Manufacturer Part"/><toAliasTarget alias="Manufacturer Part Master"/></join></referenceJoin></query></qml>