data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = file(pathexpand("~/.ssh/id_ed25519.pub"))
}

resource "aws_ebs_volume" "web" {
  availability_zone = "${var.aws_region}a"
  size              = 40

  tags = {
    Name = "Web"
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3a.medium"
  subnet_id     = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  key_name = aws_key_pair.deployer.key_name

  root_block_device {
    volume_size = 40
  }

  instance_market_options {
        market_type = "spot"
        spot_options {
          instance_interruption_behavior = "stop"
          spot_instance_type             = "persistent"
          max_price                      = "0.015" # Maximum price you are willing to pay
        }
      }

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y docker.io docker-compose git curl
              curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
              apt-get install -y nodejs
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ubuntu
              git clone https://github.com/mannu0530/CICD-pipeline-health-monitoring.git /app
              cd /app/frontend
              npm install
              npm run build
              cd /app
              docker-compose --profile production up -d
              EOF

  tags = {
    Name = "cicd-monitoring-instance"
  }
}

output "instance_public_ip" {
  value = aws_instance.web.public_ip
}