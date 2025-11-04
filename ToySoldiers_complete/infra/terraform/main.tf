terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.45"
    }
  }
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

provider "hcloud" {
  token = var.hetzner_api_token
}

# Cloudflare Zone
resource "cloudflare_zone" "toysoldiers" {
  account_id = var.cloudflare_account_id
  zone       = "toysoldiers.space"
}

# DNS Records
resource "cloudflare_record" "app" {
  zone_id = cloudflare_zone.toysoldiers.id
  name    = "app"
  value   = hcloud_server.backend.ipv4_address
  type    = "A"
  proxied = true
}

resource "cloudflare_record" "api" {
  zone_id = cloudflare_zone.toysoldiers.id
  name    = "api"
  value   = hcloud_server.backend.ipv4_address
  type    = "A"
  proxied = true
}

# R2 Buckets
resource "cloudflare_r2_bucket" "audio" {
  account_id = var.cloudflare_account_id
  name       = "toysoldiers-audio"
  location   = "WEUR"
}

resource "cloudflare_r2_bucket" "video" {
  account_id = var.cloudflare_account_id
  name       = "toysoldiers-video"
  location   = "WEUR"
}

resource "cloudflare_r2_bucket" "thumbnails" {
  account_id = var.cloudflare_account_id
  name       = "toysoldiers-thumbnails"
  location   = "WEUR"
}

# Hetzner Server
resource "hcloud_server" "backend" {
  name        = "toysoldiers-backend"
  server_type = "cpx31"
  image       = "ubuntu-22.04"
  location    = "fsn1"
  
  ssh_keys = [var.ssh_key_id]
  
  user_data = file("${path.module}/cloud-init.yaml")
  
  labels = {
    environment = var.environment
    project     = "toysoldiers"
  }
}

# Firewall
resource "hcloud_firewall" "backend" {
  name = "toysoldiers-firewall"
  
  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "22"
    source_ips = [
      "0.0.0.0/0",
      "::/0"
    ]
  }
  
  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "80"
    source_ips = [
      "0.0.0.0/0",
      "::/0"
    ]
  }
  
  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "443"
    source_ips = [
      "0.0.0.0/0",
      "::/0"
    ]
  }
}

resource "hcloud_firewall_attachment" "backend" {
  firewall_id = hcloud_firewall.backend.id
  server_ids  = [hcloud_server.backend.id]
}

# Outputs
output "backend_ip" {
  value = hcloud_server.backend.ipv4_address
}

output "cloudflare_zone_id" {
  value = cloudflare_zone.toysoldiers.id
}
