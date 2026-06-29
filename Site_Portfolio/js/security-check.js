// security-check.js
// This script must be loaded synchronously in the <head> of protected pages
// It checks if the user has a valid session token granted by index.html
(function() {
    const accessGranted = sessionStorage.getItem('unsc_access_granted');
    
    if (accessGranted !== 'true') {
        // Redirect to index.html if no valid session is found
        // Determine the correct path to index.html based on current location
        // Since all protected pages are in the same root folder, a relative path is fine.
        window.location.replace('index.html');
    }
})();
