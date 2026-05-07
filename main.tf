provider "aws" {
  region = "eu-central-1" 
}

resource "aws_security_group" "web_sg" {
  name        = "allow_web_traffic"
  description = "Permite accesul de pe internet la aplicatia noastra"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web_server" {
  ami           = "ami-04e601abe3e1a910f" 
  instance_type = "t2.micro"              # Cel mai mic server (Free Tier)

  vpc_security_group_ids = [aws_security_group.web_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update
              sudo apt-get install -y docker.io
              sudo systemctl start docker
              sudo systemctl enable docker
              
              sudo docker run -d -p 80:8000 amalia222/devops-api:latest
              EOF

  tags = {
    Name = "DevOps-Project-Server"
  }
}