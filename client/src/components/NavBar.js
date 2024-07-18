import React from "react";

function Navbar() {


    return (
            <nav class="bg-gray-800">
                <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
                    <div class="relative flex h-16 items-center justify-between">
                    <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
                        <div class="flex flex-shrink-0 items-center">
                        </div>
                        <div class="hidden sm:ml-6 sm:block">
                        <div class="flex space-x-4">
                            <a href="/" class="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white" aria-current="page">Dashboard</a>
                            <a href="https://www.medicines.org.uk/emc/" class="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white">EMC</a>
                            <a href="/" class="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white">API Key</a>
                            
                        </div>
                        </div>
                    </div>
                        <div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
                            <h1 className="navbar-title text-3xl font-bold text-gray-300">LC-Vision Pill Checker 🔎</h1>

                        </div>
                    </div>
                </div>

        </nav>
    )
};

export default Navbar;