
# LC-Vision

This is an ongoing project being built alongside the LC Pill Checker project to expand its capabilities to allow for image analysis/interpretation of tablets and capsules

## Architecture

![image](https://github.com/user-attachments/assets/2ef85dc8-a9b0-42ca-a7de-d7f28f5725ef)


## Environment Variables

To run this project, you will need to add the following environment variables to your .env files

Client:

`REACT_APP_IMG_ENDPOINT`- API endpoint to upload images to

`REACT_APP_KEY_ENDPOINT` - API endpoint to store the user's OpenAI API key

API:

`SECRET_KEY` - for flask sessions configuration

`REDIS_HOST` - Redis cloud endpoint

`REDIS_PWD` - Redis cloud endpoint password

`REDIS_PORT` - Redis cloud port

`PINECONE_API_KEY` - API key for Pinecone Vector database

`PINECONE_INDEX_NAME` - Name of index to create in Pinecone



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

**RAG:** Pinecone, OpenAI models (gpt-4o, text-embedding-3-large), LangChain, huggingface models

todo:

1. link frontend to be processed by lc backend on flask ✔️
2. fix image processing errors - fix upload and api key endpoints ✔️
3. Convert image recognition results to embeddings to query pinecone vector store ✔️
4. Test huggingface models
5. prepare images for testing
6. firebase authentication
7. set up feedback database for RLHF
