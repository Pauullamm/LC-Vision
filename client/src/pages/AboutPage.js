import React from 'react';

export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto p-6 bg-gray-800 rounded-lg shadow-lg">
      {/* Main Heading */}
      <h1 className="text-center text-3xl font-bold text-white mb-6">
        Hi there! 👋 Thanks for checking out LC-Vision 😊
      </h1>

      {/* Introduction Paragraph */}
      <p className="text-lg text-gray-300 mb-4">
        I originally had the idea of creating an application that would allow you to take a photo of an unknown tablet or capsule, and it would use image recognition to identify that pill. However, the challenge was that most pharmaceutical companies don't publish images of their tablets/capsules.
      </p>

      {/* Transition Paragraph */}
      <p className="text-lg text-gray-300 mb-4">
        So, instead, I thought of utilizing text descriptions of tablets and capsules as a way to identify them using retrieval-augmented generation (RAG). This led me to create LC-Pill Checker—a simple interface/chatbot where you can ask questions about pill descriptions.
      </p>

      {/* Use Cases */}
      <div className="bg-gray-700 p-4 rounded-lg mb-6">
        <h2 className="text-xl text-white font-semibold mb-3">Here are some example queries I've tried to ask:</h2>
        <ol className="list-inside list-decimal text-gray-300">
          <li>"What color do warfarin tablets come in?"</li>
          <li>"List out 5 tablets/capsules that are blue in color and their manufacturers"</li>
          <li>"Among these medications: *list of medications*, which ones are scored?"</li>
        </ol>
      </div>

      {/* Transition with Highlighted Text */}
      <div className="text-center text-gray-300 mb-6">
        <h2 className="text-3xl font-black italic text-white">HOWEVER...</h2>
        <p className="text-lg mb-3">A picture is worth a thousand words, right?</p>
        <p className="text-lg mb-6">
          I still wanted to find a way to incorporate image recognition into the project, so I thought, "Why not link the current RAG functionality to a user interface that describes images of pills and feed that description to the LLM?"
        </p>
        <p className="text-lg text-gray-300">And that’s how LC-Vision came into being!</p>
      </div>

      {/* Work-in-Progress Statement */}
      <div className="text-center text-gray-300 mb-6">
        <p className="italic text-lg">This is still very much a work in progress, and sometimes I have no idea what I'm doing...</p>
      </div>

      {/* GIF Section */}
      <div className="flex justify-center items-center mb-6">
        <img
          alt="tech"
          src="https://media1.giphy.com/media/NAcNfRrU6f2bC/giphy.gif"
          className="max-w-full h-auto rounded-lg"
        />
      </div>

      {/* Closing Remarks */}
      <p className="text-center text-lg text-gray-300">
        Please don't expect this to be a marketable product in any way, shape, or form 😂, but in the meantime, I hope you enjoy fiddling around with it. Feel free to send me any suggestions. Thanks!
        <br />
        - Paul
      </p>
    </div>
  );
}
