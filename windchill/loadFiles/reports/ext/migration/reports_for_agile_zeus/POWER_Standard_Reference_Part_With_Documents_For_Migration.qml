<qml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" bypassAccessControl="false" caseInsensitive="false" addTimeToDateFields="false" mainType="POWER Standard Reference Part" joinModel="false" xsi:noNamespaceSchemaLocation="qml.xsd"><query><selectOrConstrain distinct="false" group="false"><reportAttribute heading="Std Ref Part Number" reportAttributeId="Number_2" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Standard Reference Part" isExternal="false" type="java.lang.String" propertyName="number">master&gt;number</column></reportAttribute><reportAttribute heading="Std Ref Part Name" reportAttributeId="Name_2" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Standard Reference Part" isExternal="false" type="java.lang.String" propertyName="name">master&gt;name</column></reportAttribute><reportAttribute heading="Std Ref Part Organization Name" reportAttributeId="Organization_Name_organizationName__1" userCanSelect="true" userCanConstrain="false" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><object alias="POWER Standard Reference Part" propertyName="organizationName"/></reportAttribute><reportAttribute heading="Std Ref Part Version" reportAttributeId="versionInfo_identifier_versionId_1" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Standard Reference Part" isExternal="false" type="java.lang.String" propertyName="versionInfo.identifier.versionId">versionInfo.identifier.versionId</column></reportAttribute><reportAttribute heading="Std Ref Part State" reportAttributeId="State_1" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Standard Reference Part" isExternal="false" type="wt.lifecycle.State" propertyName="lifeCycleState">state.state</column></reportAttribute><reportAttribute heading="Std Ref Part Created" reportAttributeId="Created" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Standard Reference Part" isExternal="false" type="java.sql.Timestamp" propertyName="createTimestamp">thePersistInfo.createStamp</column></reportAttribute><reportAttribute heading="Std Ref Part Modified" reportAttributeId="Last_Modified" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Standard Reference Part" isExternal="false" type="java.sql.Timestamp" propertyName="modifyTimestamp">thePersistInfo.modifyStamp</column></reportAttribute><reportAttribute heading="Std Ref Part Iteration Note" reportAttributeId="Iteration_Note_1" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="POWER Standard Reference Part" isExternal="false" type="java.lang.String" propertyName="iterationNote">iterationInfo.note</column></reportAttribute><reportAttribute heading="Doc Number" reportAttributeId="Number" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="Document Master" isExternal="false" type="java.lang.String" propertyName="number">number</column></reportAttribute><reportAttribute heading="Doc Name" reportAttributeId="Name" userCanSelect="true" userCanConstrain="true" alwaysSelect="false" defaultValue="" constantValue="" isMacro="false"><column alias="Document Master" isExternal="false" type="java.lang.String" propertyName="name">name</column></reportAttribute></selectOrConstrain><from><table alias="Document Master" isExternal="false" xposition="38px" yposition="269px">wt.doc.WTDocumentMaster</table><table alias="POWER Standard Reference Part" isExternal="false" xposition="221px" yposition="25px">WCTYPE|com.ptc.windchill.suma.part.ManufacturerPart|ext.lps.LPSManufacturerPart|ext.lps.power.POWERStandardReferencePart</table></from><where><compositeCondition type="and"><condition><standardCondition><operand><column alias="POWER Standard Reference Part" isExternal="false" type="boolean" propertyName="latestIteration">iterationInfo.latest</column></operand><operator type="equal"/><operand><constant type="java.lang.String" isMacro="false" xml:space="preserve">1</constant></operand></standardCondition></condition><condition><standardCondition><operand><column alias="POWER Standard Reference Part" isExternal="false" type="java.lang.String" propertyName="iterationNote">iterationInfo.note</column></operand><operator type="like"/><operand><constant type="java.lang.String" isMacro="false" xml:space="preserve">%</constant></operand></standardCondition></condition></compositeCondition></where><orderBy><orderByItem type="asc"><reportAttributeReference id="Number_2"/></orderByItem></orderBy><linkJoin><join name="wt.part.WTPartDocumentLink" outerJoinAlias="Document Master"><fromAliasTarget alias="POWER Standard Reference Part"/><toAliasTarget alias="Document Master"/></join></linkJoin></query></qml>