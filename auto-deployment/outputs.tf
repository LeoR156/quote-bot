output "public_ip_server_1" {
  value       = yandex_compute_instance.servers[0].network_interface.0.nat_ip_address
  description = "Белый IP первого сервера"
}
output "internal_ips" {
  value       = yandex_compute_instance.servers[*].network_interface.0.ip_address
  description = "Внутренние IP адреса обоих серверов"
}
