from crossplane.function import resource
from crossplane.function.proto.v1 import run_function_pb2 as fnv1

from model.io.upbound.platform.aws.xnetwork import v1alpha1 as v1alpha1
from model.io.upbound.aws.ec2.vpc import v1beta1 as v1beta1vpc

import typing

def compose(req: fnv1.RunFunctionRequest, rsp: fnv1.RunFunctionResponse):
    region = "us-west-1"
    deletionPolicy = v1alpha1.DeletionPolicy.Delete
    
    observed_xr = v1alpha1.XNetwork(**req.observed.composite.resource)
    
    if observed_xr.spec.deletionPolicy is not None:
        deletionPolicy = observed_xr.spec.deletionPolicy
    
    if observed_xr.spec.region is not None:
        region = observed_xr.spec.region
        
        vpc = v1beta1vpc.VPC( 
            spec = v1beta1vpc.Spec(
                deletionPolicy=deletionPolicy,
                forProvider = v1beta1vpc.ForProvider(
                    region = region,
                    enableDnsHostnames=True,
                    enableDnsSupport=True,
                ),     
            )       
        )
        vpc.spec.forProvider.tags = {"Name":observed_xr.metadata.name}

    resource.update(rsp.desired.resources["vpc"], vpc)
    return rsp
