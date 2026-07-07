provider "aws" {
  region = "eu-central-1" 
}

resource "aws_security_group" "web_sg" {
  name        = "allow_web_traffic"
  description = "Permite accesul de pe internet la aplicatie"

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

//rolul pentru server
resource "aws_iam_role" "ec2_ssm_role" {
  name = "ec2_ssm_role"
  //cine are voie sa foloseasca acest rol? 
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    //reguli
    Statement = [{
      Action = "sts:AssumeRole" //security token service 
      Effect = "Allow" // pentru a permite actiunea de dinainte 
      Principal = { Service = "ec2.amazonaws.com" } //cine primeste aceasta permisiune
    }]
  })
}

//adaug permisiunea de ssm 
resource "aws_iam_role_policy_attachment" "ssm_policy_attach"{
  role = aws_iam_role.ec2_ssm_role.name
  // amazon resource name (este unic pentru fiecare obiect din aws) 
  policy_arn = "arn:aws:iam:aws::policy/AmazonSSMManagedInstanceCore"
}

//impachetare rol in instanta pentru a fi pus pe server
resource "aws_iam_instance_profile" "ec2_ssm_profile"{
  name = "ec2_ssm_profile"
  role = aws_iam_role.ec2_ssm_role.name 
}

resource "aws_instance" "web_server" {
  ami           = "ami-04e601abe3e1a910f" 
  instance_type = "t2.micro"          

  vpc_security_group_ids = [aws_security_group.web_sg.id]

  iam_instance_profile = aws_iam_instance_profile.ec2_ssm_profile.name

  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update
              sudo apt-get install -y docker.io
              sudo systemctl start docker
              sudo systemctl enable docker
              
              sudo docker run -d -p 80:8000 amalia222/devops-api:latest
              EOF

  tags = {
    Name = "Project-Ama"
  }
}