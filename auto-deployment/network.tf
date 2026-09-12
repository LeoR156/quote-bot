resource "yandex_vpc_network" "network" {
  name = "my-network"
}

resource "yandex_vpc_subnet" "subnet" {
  name           = "my-internal-subnet"
  v4_cidr_blocks = ["10.0.0.0/24"]
  zone           = "ru-central1-d"
  network_id     = yandex_vpc_network.network.id
}
