variable "location" {
  description = "Azure region for resources"
  default     = "Canada East"
}

variable "resource_group_name" {
  description = "Name of the resource group"
  default     = "automate-all-the-things-rg"
}

variable "aks_cluster_name" {
  description = "Name of the AKS cluster"
  default     = "automate-aks-cluster"
}

variable "acr_name" {
  description = "Name of the Azure Container Registry"
  default     = "automateacr"
}

variable "node_count" {
  description = "Number of nodes in the AKS cluster"
  type        = number
  default     = 3
  validation {
    condition     = var.node_count > 0
    error_message = "Node count must be greater than 0."
  }
}

variable "vnet_name" {
  description = "Name of the virtual network"
  default     = "automate-vnet"
}

variable "subnet_name" {
  description = "Name of the subnet for AKS"
  default     = "automate-subnet"
}

variable "address_space" {
  description = "CIDR block for the virtual network"
  default     = ["10.0.0.0/16"]
}

variable "subnet_address_prefix" {
  description = "CIDR block for the subnet"
  default     = "10.0.1.0/24"
}