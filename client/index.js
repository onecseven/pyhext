// Importing .env file
require('dotenv').config()

// External libraries
const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const port = process.env.PORT;
const server = http.createServer(express);
const wss = new WebSocket.Server({ server });
