# Add OffHour/OnHour Filter Support for Kubernetes Resources

## Summary
- Add OffHour and OnHour filter support to Kubernetes resources for scheduled cost optimization
- Enable off-hours scaling/shutdown capabilities across Deployment, StatefulSet, DaemonSet, ReplicaSet, Pod, and Custom Resource types
- Provide comprehensive test coverage for filter registration and policy validation

## Changes Made
- **Resource Filter Registration**: Added OffHour/OnHour filter imports and registrations to:
  - `tools/c7n_kube/c7n_kube/resources/apps/deployment.py`
  - `tools/c7n_kube/c7n_kube/resources/apps/statefulset.py`
  - `tools/c7n_kube/c7n_kube/resources/apps/daemonset.py`
  - `tools/c7n_kube/c7n_kube/resources/apps/replicaset.py`
  - `tools/c7n_kube/c7n_kube/resources/core/pod.py`
  - `tools/c7n_kube/c7n_kube/resources/crd.py`

- **Test Coverage**: Added comprehensive tests in `tools/c7n_kube/tests/test_actions.py`:
  - Filter registration validation for all resource types
  - Policy validation tests for offhour/onhour configurations
  - Integration tests ensuring proper functionality

## Use Cases
This enhancement enables cost optimization scenarios such as:

```yaml
# Scale down deployments during off-hours (7PM ET)
policies:
  - name: deployment-offhours-scale-down
    resource: k8s.deployment
    filters:
      - type: offhour
        default_tz: et
        offhour: 19
    actions:
      - type: patch
        options:
          spec:
            replicas: 0

# Scale up deployments during on-hours (7AM ET)
policies:
  - name: deployment-onhours-scale-up
    resource: k8s.deployment
    filters:
      - type: onhour
        default_tz: et
        onhour: 7
    actions:
      - type: patch
        options:
          spec:
            replicas: 3
```

## Test Plan
- [x] All resource types properly register OffHour/OnHour filters
- [x] Policy validation works correctly for offhour/onhour configurations
- [x] Integration with existing Cloud Custodian offhours functionality
- [x] Comprehensive test coverage for all supported resource types

## Related Issues
- Addresses community need for Kubernetes cost optimization capabilities
- Aligns with Cloud Custodian's mission of cloud resource governance and cost management
- Extends existing offhours functionality to Kubernetes resources

🤖 Generated with [Claude Code](https://claude.ai/code)