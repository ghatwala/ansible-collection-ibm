#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ibm_iam_trusted_profile_claim_rule
for_more_info:  refer - https://registry.terraform.io/providers/IBM-Cloud/ibm/latest/docs/resources/iam_trusted_profile_claim_rule

short_description: Configure IBM Cloud 'ibm_iam_trusted_profile_claim_rule' resource

version_added: "2.8"

description:
    - Create, update or destroy an IBM Cloud 'ibm_iam_trusted_profile_claim_rule' resource
    - This module supports idempotency
requirements:
    - IBM-Cloud terraform-provider-ibm v1.35.0
    - Terraform v0.12.20

options:
    cr_type:
        description:
            - The compute resource type the rule applies to, required only if type is specified as 'Profile-CR'. Valid values are VSI, IKS_SA, ROKS_SA.
        required: False
        type: str
    type:
        description:
            - (Required for new resource) Type of the calim rule, either 'Profile-SAML' or 'Profile-CR'.
        required: True
        type: str
    realm_name:
        description:
            - The realm name of the Idp this claim rule applies to. This field is required only if the type is specified as 'Profile-SAML'.
        required: False
        type: str
    expiration:
        description:
            - Session expiration in seconds, only required if type is 'Profile-SAML'.
        required: False
        type: int
    profile_id:
        description:
            - (Required for new resource) ID of the trusted profile to create a claim rule.
        required: True
        type: str
    conditions:
        description:
            - (Required for new resource) Conditions of this claim rule.
        required: True
        type: list
        elements: dict
    name:
        description:
            - Name of the claim rule to be created or updated.
        required: False
        type: str
    id:
        description:
            - (Required when updating or destroying existing resource) IBM Cloud Resource ID.
        required: False
        type: str
    state:
        description:
            - State of resource
        choices:
            - available
            - absent
        default: available
        required: False
    iaas_classic_username:
        description:
            - (Required when generation = 1) The IBM Cloud Classic
              Infrastructure (SoftLayer) user name. This can also be provided
              via the environment variable 'IAAS_CLASSIC_USERNAME'.
        required: False
    iaas_classic_api_key:
        description:
            - (Required when generation = 1) The IBM Cloud Classic
              Infrastructure API key. This can also be provided via the
              environment variable 'IAAS_CLASSIC_API_KEY'.
        required: False
    region:
        description:
            - The IBM Cloud region where you want to create your
              resources. If this value is not specified, us-south is
              used by default. This can also be provided via the
              environment variable 'IC_REGION'.
        default: us-south
        required: False
    ibmcloud_api_key:
        description:
            - The IBM Cloud API key to authenticate with the IBM Cloud
              platform. This can also be provided via the environment
              variable 'IC_API_KEY'.
        required: True

author:
    - Jay Carman (@jaywcarman)
'''

# Top level parameter keys required by Terraform module
TL_REQUIRED_PARAMETERS = [
    ('type', 'str'),
    ('profile_id', 'str'),
    ('conditions', 'list'),
]

# All top level parameter keys supported by Terraform module
TL_ALL_PARAMETERS = [
    'cr_type',
    'type',
    'realm_name',
    'expiration',
    'profile_id',
    'conditions',
    'name',
]

# Params for Data source
TL_REQUIRED_PARAMETERS_DS = [
    ('profile_id', 'str'),
    ('rule_id', 'str'),
]

TL_ALL_PARAMETERS_DS = [
    'profile_id',
    'rule_id',
]

TL_CONFLICTS_MAP = {
}

# define available arguments/parameters a user can pass to the module
from ansible_collections.ibm.cloudcollection.plugins.module_utils.ibmcloud import Terraform, ibmcloud_terraform
from ansible.module_utils.basic import env_fallback
module_args = dict(
    cr_type=dict(
        required=False,
        type='str'),
    type=dict(
        required=False,
        type='str'),
    realm_name=dict(
        required=False,
        type='str'),
    expiration=dict(
        required=False,
        type='int'),
    profile_id=dict(
        required=False,
        type='str'),
    conditions=dict(
        required=False,
        elements='',
        type='list'),
    name=dict(
        required=False,
        type='str'),
    id=dict(
        required=False,
        type='str'),
    state=dict(
        type='str',
        required=False,
        default='available',
        choices=(['available', 'absent'])),
    iaas_classic_username=dict(
        type='str',
        no_log=True,
        fallback=(env_fallback, ['IAAS_CLASSIC_USERNAME']),
        required=False),
    iaas_classic_api_key=dict(
        type='str',
        no_log=True,
        fallback=(env_fallback, ['IAAS_CLASSIC_API_KEY']),
        required=False),
    region=dict(
        type='str',
        fallback=(env_fallback, ['IC_REGION']),
        default='us-south'),
    ibmcloud_api_key=dict(
        type='str',
        no_log=True,
        fallback=(env_fallback, ['IC_API_KEY']),
        required=True)
)


def run_module():
    from ansible.module_utils.basic import AnsibleModule

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # New resource required arguments checks
    missing_args = []
    if module.params['id'] is None:
        for arg, _ in TL_REQUIRED_PARAMETERS:
            if module.params[arg] is None:
                missing_args.append(arg)
        if missing_args:
            module.fail_json(msg=(
                "missing required arguments: " + ", ".join(missing_args)))

    conflicts = {}
    if len(TL_CONFLICTS_MAP) != 0:
        for arg in TL_CONFLICTS_MAP:
            if module.params[arg]:
                for conflict in TL_CONFLICTS_MAP[arg]:
                    try:
                        if module.params[conflict]:
                            conflicts[arg] = conflict
                    except KeyError:
                        pass
    if len(conflicts):
        module.fail_json(msg=("conflicts exist: {}".format(conflicts)))

    result_ds = ibmcloud_terraform(
        resource_type='ibm_iam_trusted_profile_claim_rule',
        tf_type='data',
        parameters=module.params,
        ibm_provider_version='1.35.0',
        tl_required_params=TL_REQUIRED_PARAMETERS_DS,
        tl_all_params=TL_ALL_PARAMETERS_DS)

    if result_ds['rc'] != 0 or (result_ds['rc'] == 0 and (module.params['id'] is not None or module.params['state'] == 'absent')):
        result = ibmcloud_terraform(
            resource_type='ibm_iam_trusted_profile_claim_rule',
            tf_type='resource',
            parameters=module.params,
            ibm_provider_version='1.35.0',
            tl_required_params=TL_REQUIRED_PARAMETERS,
            tl_all_params=TL_ALL_PARAMETERS)
        if result['rc'] > 0:
            module.fail_json(
                msg=Terraform.parse_stderr(result['stderr']), **result)

        module.exit_json(**result)
    else:
        module.exit_json(**result_ds)


def main():
    run_module()


if __name__ == '__main__':
    main()