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
  


  # Указываем загрузочный диск с Ubuntu
  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.ubuntu.id
      size     = 10 # Размер загрузочного диска
    }
  }
  # Подключаем наш общий диск на 30 ГБ
  filesystem {
    filesystem_id = yandex_compute_filesystem.shared_disk.id
    device_name   = "shared-disk"
  }
  # Подключаем сервер к подсети (которая лежит в файле network.tf)
  network_interface {
    subnet_id = yandex_vpc_subnet.subnet.id
    
    # Даем белый IP только первому серверу
    nat = count.index == 0 ? true : false
  }
}