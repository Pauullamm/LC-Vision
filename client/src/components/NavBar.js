import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux';
import { setInputValue } from "../redux/actions";
//routing
import { Link } from "react-router-dom";

function Navbar() {
    const [apiSectionOpen, setApiSectionOpen] = useState(false);
    const dispatch = useDispatch();
    const inputValue = useSelector((state) => state.input.inputValue);
    const [menuOpen, setMenuOpen] = useState(false);
    useEffect(() => {
        const handleResize = () => {
            if (window.innerWidth >=768) {
                setMenuOpen(false);
            } else {
                setMenuOpen(true);
                toggleMenu();
            }
        };
        window.addEventListener('resize', handleResize);

        
    }, []);
    
    const toggleMenu = () => {
        setMenuOpen(prevState => !prevState);
    }

    const toggleApiInput = () => {
        setApiSectionOpen(prevState => !prevState)
    };

    const handleInputChange = (event) => {
        dispatch(setInputValue(event.target.value));
    };

    const handleKeyDown = async (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const formData = new FormData();
            formData.append('input', inputValue);
            const port = process.env.REACT_APP_KEY_ENDPOINT
            try {
                const response = await fetch(port, {
                    method: 'POST',
                    body: formData
                });
                if (response.ok) {
                    console.log(response);
                } else {
                    console.error('Error submitting data');
                };
            } catch (error) {
                console.error('Error:', error);
            }
        }
    }

    return (
            <nav className="bg-gray-900">
                <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
                    <div className="relative flex h-16 items-center justify-between">
                        <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
                            <button type="button" 
                            class="relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white" 
                            aria-controls="mobile-menu" 
                            aria-expanded="false"
                            onClick={toggleMenu}>
                            <span class="absolute -inset-0.5"></span>
                            <span class="sr-only">Open main menu</span>

                            <svg class="block h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                            </svg>

                            <svg class="hidden h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                            </button>
                        </div>
                    <div className="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">

                        <div className="hidden sm:ml-5 sm:block">
                        {!menuOpen && (<div className="flex space-x-3">
                            <Link to='/' className="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white">Home</Link>
                            <Link to='/about' className="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white">About</Link>
                            <a href="https://www.medicines.org.uk/emc/" target="_blank" rel="noopener noreferrer" className="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white">EMC</a>
                            <button className="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white" onClick={toggleApiInput}>API Key</button>
                            <div className={`inputSection ${apiSectionOpen ? "open": ""} content-center`}>
                                <input className="content-center 
                                appearance-none 
                                py-1 px-2 
                                border border-black-500 
                                rounded w-full text-gray-700 leading-tight 
                                focus:outline-none focus:shadow-outline" 
                                id="password" 
                                type="password" 
                                placeholder="Enter API Key"
                                onChange={handleInputChange}
                                onKeyDown={handleKeyDown}
                                />
                            </div>
                        </div>)}
                        </div>
                    </div>
                        <div className="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0" >
                            <h2 className="navbar-title text-3xl font-black italic text-gray-300">LC-Vision Pill Checker </h2>
                            <h2 className="navbar-title text-3xl font-black text-gray-300">🔎</h2>

                        </div>
                        
                    </div>
                </div>
                {/* <!-- Mobile menu, show/hide based on menu state. --> */}
                <div>

                        {menuOpen && (<div className="flex py-5 px-2">
                            <Link to='/' className=" rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white">Home</Link>
                            <Link to='/about' className=" rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white">About</Link>
                            <a href="https://www.medicines.org.uk/emc/" target="_blank" rel="noopener noreferrer" className="  rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white">EMC</a>
                            <button className="  rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white" onClick={toggleApiInput}>API Key</button>
                            <div className={` inputSection ${apiSectionOpen ? "open": ""} content-center`}>
                                <input className="
                                content-center 
                                appearance-none 
                                py-1 px-2 
                                mx-2
                                border border-black-500 
                                rounded w-full text-gray-700 leading-tight 
                                focus:outline-none focus:shadow-outline" 
                                id="password" 
                                type="password" 
                                placeholder="Enter API Key"
                                onChange={handleInputChange}
                                onKeyDown={handleKeyDown}
                                />
                            </div>
                        </div>)
                        }
                    </div>
        </nav>
    )
};

export default Navbar;