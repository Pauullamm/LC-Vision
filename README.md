
# LC-Vision

This is an ongoing project being built alongside the LC Pill Checker project to expand its capabilities to allow for image analysis

## Architecture

![diagram-export-01-08-2024-20_10_11](https://github.com/user-attachments/assets/d69b9a9a-364c-4745-b36e-6038186d2047)

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`REACT_APP_IMG_ENDPOINT`- API endpoint to upload images to

`REACT_APP_KEY_ENDPOINT` - API endpoint to store the user's OpenAI API key

`SECRET_KEY` - for flask sessions configuration

`REDIS_HOST` - Redis cloud endpoint

`REDIS_PWD` - Redis cloud endpoint password

`REDIS_PORT` - Redis cloud port



## Flask API endpoints

#### Send API key

```http
  POST /key
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `input` | `string` | (**Required**) Your OpenAI API key |

#### Send image

```http
  POST /upload
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `images`      | `object (form-data)` | (**Required**) Image to analyse |


## Tech Stack

**Client:** React, Redux, TailwindCSS

**Server:** Flask, Render, Redis


todo:

1. set up feedback database for RLHF
2. link frontend to be processed by lc backend on flask
3. fix image processing errors - fix upload and api key endpoints
4. prepare images for testing
