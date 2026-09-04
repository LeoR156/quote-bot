resource "yandex_compute_filesystem" "shared_disk" {
  name = "my-shared-30gb-disk"
  type = "network-hdd"
  size = 30
  zone = "ru-central1-d"
}

data "yandex_compute_image" "ubuntu" {
  family = "ubuntu-2404-lts"
}

resource "yandex_compute_instance" "servers" {
  count = 2
  name        = "server-${count.index + 1}"
  platform_id = "standard-v3"
  zone        = "ru-central1-d"

  resources {
    cores  = 2
    memory = 2
  }
  
}
