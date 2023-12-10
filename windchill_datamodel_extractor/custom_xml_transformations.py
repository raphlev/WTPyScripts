class CustomXMLTransformations:
    @staticmethod
    def normalize_xml(xml_content):
            # Define the replacements as a list of tuples to be executed in same order
            replacements = [
            # TYPES, CLASSIFICATION
                ('</csvBeginTypes>', ''),
                ('<csvBeginTypes handler="com.ptc.core.lwc.server.TypeDefinitionLoader.beginProcessTypes"/>', '<csvBeginTypes handler="com.ptc.core.lwc.server.TypeDefinitionLoader.beginProcessTypes">'),
                ('</csvBeginTypeDefView>', ''),
                ('</csvBeginLayoutDefView>', ''),
                ('</csvBeginGroupDefView>', ''),
                ('</csvBeginGroupMemberView>', ''),
                ('</csvBeginAttributeDefView>', ''),
                ('</csvBeginConstraintDefView>', ''),
                ('</csvBeginEnumDefView>', ''),
                ('</csvBeginEnumMemberView>', ''),
                ('<csvEndEnumMemberView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessEnumMembership"/>', '</csvBeginEnumMemberView>'),
                ('<csvEndEnumMemberView handler="com.ptc.core.lwc.server.BaseDefinitionLoader.endProcessEnumMembership"/>', '</csvBeginEnumMemberView>'),
                ('<csvEndEnumDefView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessEnumerationDefinition"/>', '</csvBeginEnumDefView>'),
                ('<csvEndEnumDefView handler="com.ptc.core.lwc.server.BaseDefinitionLoader.endProcessEnumerationDefinition"/>', '</csvBeginEnumDefView>'),
                ('<csvEndConstraintDefView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessConstraintDefinition"/>', '</csvBeginConstraintDefView>'),
                ('<csvEndAttributeDefView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessAttributeDefinition"/>', '</csvBeginAttributeDefView>'),
                ('<csvEndGroupMemberView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessGroupMembership"/>', '</csvBeginGroupMemberView>'),
                ('<csvEndGroupDefView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessGroupDefinition"/>', '</csvBeginGroupDefView>'),
                ('<csvEndLayoutDefView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessLayoutDefinition"/>', '</csvBeginLayoutDefView>'),
                ('<csvEndTypeDefView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessTypeDefinition"/>', '</csvBeginTypeDefView>'),
                ('<csvEndTypes handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessTypes"/>', '</csvBeginTypes>'),
            # LIFECYCLE
                ('</csvLifeCycleTemplateBegin>', ''),
                ('<csvPhaseTemplateEnd handler="wt.lifecycle.LoadLifeCycle.createPhaseTemplateEnd"></csvPhaseTemplateEnd>', ''),
                ('<csvLifeCycleTemplateEnd handler="wt.lifecycle.LoadLifeCycle.createLifeCycleTemplateEnd"></csvLifeCycleTemplateEnd>', '</csvLifeCycleTemplateBegin>'),
                ('<csvLifeCycleTemplateEnd handler="wt.lifecycle.LoadLifeCycle.createLifeCycleTemplateEnd"/>', '</csvLifeCycleTemplateBegin>'),
            # OIR
                ('<![CDATA[', ''),
                (']]>', ''),
            ]
    
            # Perform the replacements in order
            for old, new in replacements:
                xml_content = xml_content.replace(old, new)
    
            return xml_content
    
        