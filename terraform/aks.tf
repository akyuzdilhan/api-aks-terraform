resource "azurerm_kubernetes_cluster" "aks" {
  name                = "automate-aks-cluster"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "automate-aks"

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "Standard_B2s"
    vnet_subnet_id = azurerm_subnet.subnet.id
  }

  network_profile {
    network_plugin     = "azure"
    service_cidr       = "10.1.0.0/16"     # Ensure this does not overlap with any existing subnet CIDRs
    dns_service_ip     = "10.1.0.10"      # Must be within the service_cidr range
    docker_bridge_cidr = "172.17.0.1/16"  # Default Docker bridge CIDR
  }

  identity {
    type        = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.aks_identity.id]
  }

  depends_on = [
    azurerm_role_assignment.acr_pull_role,
    azurerm_role_assignment.contributor_role
  ]
}

resource "azurerm_user_assigned_identity" "aks_identity" {
  name                = "automate-aks-identity"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
}

resource "azurerm_role_assignment" "acr_pull_role" {
  principal_id         = azurerm_user_assigned_identity.aks_identity.principal_id
  role_definition_name = "AcrPull"
  scope                = azurerm_container_registry.acr.id
}

resource "azurerm_role_assignment" "contributor_role" {
  principal_id         = azurerm_user_assigned_identity.aks_identity.principal_id
  role_definition_name = "Contributor"
  scope                = azurerm_resource_group.rg.id
}
