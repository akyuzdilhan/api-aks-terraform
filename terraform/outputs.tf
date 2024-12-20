output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}

output "subnet_id" {
  value = azurerm_subnet.subnet.id
}

output "kubeconfig" {
  value = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}

output "app_service_ip" {
  value = kubernetes_service.app_service.status
  description = "The status block of the LoadBalancer service for debugging purposes."
}