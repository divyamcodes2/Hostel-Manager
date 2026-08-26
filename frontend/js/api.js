const API_BASE_URL = "http://127.0.0.1:5000/api";


async function apiRequest(endpoint, options = {}) {

    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
        {
            ...options,

            credentials: "include",

            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {})
            }
        }
    );


    let data;

    try {

        data = await response.json();

    } catch (error) {

        throw new Error(
            "The server returned an invalid response."
        );

    }


    if (!response.ok) {

        throw new Error(
            data.error ||
            "Something went wrong."
        );

    }


    return data;

}


// ==========================================
// AUTH
// ==========================================

async function login(email, password) {

    return await apiRequest(
        "/auth/login",
        {
            method: "POST",

            body: JSON.stringify({
                email: email,
                password: password
            })
        }
    );

}


async function getCurrentUser() {

    return await apiRequest(
        "/auth/me"
    );

}


async function logout() {

    return await apiRequest(
        "/auth/logout",
        {
            method: "POST"
        }
    );

}


// ==========================================
// STUDENT COMPLAINTS
// ==========================================

async function createComplaint(
    category,
    title,
    description
) {

    return await apiRequest(
        "/complaints",
        {
            method: "POST",

            body: JSON.stringify({
                category: category,
                title: title,
                description: description
            })
        }
    );

}


async function getMyComplaints() {

    return await apiRequest(
        "/complaints"
    );

}


async function getComplaint(
    complaintId
) {

    return await apiRequest(
        `/complaints/${complaintId}`
    );

}


// ==========================================
// EXPOSE FUNCTIONS GLOBALLY
// ==========================================

window.apiRequest = apiRequest;

window.login = login;

window.getCurrentUser = getCurrentUser;

window.logout = logout;

window.createComplaint = createComplaint;

window.getMyComplaints = getMyComplaints;

window.getComplaint = getComplaint;