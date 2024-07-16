import React, { useState } from "react";

function SideBar() {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };
    
    return (
        <div>
            <h2>Sidebar Content</h2>
            <p>This is the content of the sidebar.</p>
        </div>
    )
}

export default SideBar