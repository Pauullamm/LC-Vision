import React from 'react';

export default function AboutPage() {
return (
<div className='flex flex-col'>
    <h1 className="text-center text-2xl font-bold text-gray-300">
    Hi there! 👋 Thanks for checking out LC-Vision 😊
    </h1>
    <br />
    <p className="text-center text-lg font-medium text-gray-300">
    I originally had the idea of creating an application which would allow one to 
    take a photo of an unknown tablet or capsule, and it would use image recognition to identify that unknown pill. 
    <br />
    However, the issue is that most pharmaceutical companies do not publish images of their tablets/capsules.
    <br />
    So instead, I thought of utilizing text descriptions of tablets and capsules as a means to identify them using retrieval augmented generation (RAG). This led me to make LC-Pill Checker, a simple interface/chatbot where one can ask an LLM questions about pill descriptions.
    <br />
    
    <br />
    This was useful as you could be flexible in how you ask it questions too such as:
    <br />
    </p>
    <div className="text-center text-lg font-medium text-gray-300">
    <ol>
        <li>"What color do warfarin tablets come in?"</li>
        <li>"List out 5 tablets/capsules that are blue in color as well as their manufacturers"</li>
        <li>"Among these medications *list of medications*, which one of these are scored?"</li>
    </ol>
    </div>

    <div className='flex flex-col text-center text-gray-300 text-lg font-medium'>
        <h1 className='text-3xl font-black italic'>HOWEVER</h1>
        <p>We know that a picture is worth a thousand words</p>
        <p>I decided that this was not the end of the project and still wanted to find a way to incorporate image recognition in the loop</p>

        <p>So I thought to myself, "why not link the current RAG functionality to a user interface which describes images of pills and feed that description to the LLM?" </p>
        <br />
        <p>And with that, LC-Vision came into being</p>
        
    </div>
    <p className='text-center text-gray-300 text-lg font-medium'>This is still very much a work in progress, and sometimes I have no idea what I'm doing</p>
    <div className='flex justify-center items-center'>
        <img alt='tech' src='https://media1.giphy.com/media/NAcNfRrU6f2bC/giphy.gif' className='h-1/5 w-1/5'></img>
    </div>
    <br />
    <p className='text-center text-gray-300 text-lg font-medium'>So please don't expect this to be a marketable product in any way, shape, or form hahaha, but in the meantime, I hope you'll enjoy fiddling around with it, please let me know if you have any suggestions, thank you!
    - Paul
    </p>

</div>
);
}
