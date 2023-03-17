provider "aws" {
    profile = "default"
    region = "us-east-1"
}

resource "s3_bucket" "raw" {
  bucket = "raw"
}

resource "s3_bucket" "trusted" {
  bucket = "trusted"
}

resource "s3_bucket" "refined" {
  bucket = "refined"
}