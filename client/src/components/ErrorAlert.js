import React from 'react';
import { Alert, AlertTitle } from '@mui/material';

export default function ErrorAlert({ alertText }) {
  return (
    <div>
      <Alert
        severity="error"
        sx={{
          color: "white",
          width: "50%",
          maxWidth: "50%",
          position: "absolute",
          bottom: "16px",
          left: "16px",
        }}
        variant="outlined"
      >
        <AlertTitle>Error</AlertTitle>
        {alertText} 
      </Alert>
    </div>
  );
}
