#!/bin/bash
gunicorn app:app -b :5000