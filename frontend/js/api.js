const API_BASE_URL =
    "http://127.0.0.1:5000/api";


// ============================================================
// GENERIC API REQUEST
// ============================================================

async function apiRequest(
    endpoint,
    options = {}
) {

    const response =
        await fetch(
            `${API_BASE_URL}${endpoint}`,
            {
                ...options,

                credentials:
                    "include",

                headers: {

                    "Content-Type":
                        "application/json",

                    ...(options.headers || {})

                }

            }
        );


    let data;


    try {

        data =
            await response.json();

    }
    catch (error) {

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


// ============================================================
// AUTH
// ============================================================

async function login(
    email,
    password
) {

    return await apiRequest(
        "/auth/login",
        {

            method:
                "POST",

            body:
                JSON.stringify({

                    email:
                        email,

                    password:
                        password

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

            method:
                "POST"

        }
    );

}


// ============================================================
// STUDENT COMPLAINTS
// ============================================================

async function createComplaint(
    category,
    title,
    description
) {

    return await apiRequest(
        "/complaints",
        {

            method:
                "POST",

            body:
                JSON.stringify({

                    category:
                        category,

                    title:
                        title,

                    description:
                        description

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


// ============================================================
// WARDEN COMPLAINTS
// ============================================================

async function getWardenComplaints() {

    return await apiRequest(
        "/warden/complaints"
    );

}


async function updateWardenComplaintStatus(
    complaintId,
    status
) {

    return await apiRequest(
        `/warden/complaints/${complaintId}`,
        {

            method:
                "PATCH",

            body:
                JSON.stringify({

                    status:
                        status

                })

        }
    );

}


// ============================================================
// ADMIN USERS
// ============================================================

async function getAdminUsers() {

    return await apiRequest(
        "/admin/users"
    );

}


async function createAdminUser(
    name,
    email,
    password,
    role
) {

    return await apiRequest(
        "/admin/users",
        {

            method:
                "POST",

            body:
                JSON.stringify({

                    name:
                        name,

                    email:
                        email,

                    password:
                        password,

                    role:
                        role

                })

        }
    );

}


async function updateAdminUserStatus(
    userId,
    active
) {

    return await apiRequest(
        `/admin/users/${userId}/status`,
        {

            method:
                "PATCH",

            body:
                JSON.stringify({

                    active:
                        active

                })

        }
    );

}


// ============================================================
// ADMIN ROOMS
// ============================================================

async function getAdminRooms() {

    return await apiRequest(
        "/admin/rooms"
    );

}


async function createAdminRoom(
    hostelBlock,
    roomNumber,
    capacity
) {

    return await apiRequest(
        "/admin/rooms",
        {

            method:
                "POST",

            body:
                JSON.stringify({

                    hostel_block:
                        hostelBlock,

                    room_number:
                        roomNumber,

                    capacity:
                        Number(capacity)

                })

        }
    );

}


async function assignStudentToRoom(
    userId,
    roomId
) {

    return await apiRequest(
        `/admin/users/${userId}/room`,
        {

            method:
                "PATCH",

            body:
                JSON.stringify({

                    room_id:
                        Number(roomId)

                })

        }
    );

}


async function removeStudentFromRoom(
    userId
) {

    return await apiRequest(
        `/admin/users/${userId}/room`,
        {

            method:
                "PATCH",

            body:
                JSON.stringify({

                    room_id:
                        null

                })

        }
    );

}


// ============================================================
// EXPOSE FUNCTIONS GLOBALLY
// ============================================================

window.apiRequest =
    apiRequest;


window.login =
    login;


window.getCurrentUser =
    getCurrentUser;


window.logout =
    logout;


window.createComplaint =
    createComplaint;


window.getMyComplaints =
    getMyComplaints;


window.getComplaint =
    getComplaint;


window.getWardenComplaints =
    getWardenComplaints;


window.updateWardenComplaintStatus =
    updateWardenComplaintStatus;


window.getAdminUsers =
    getAdminUsers;


window.createAdminUser =
    createAdminUser;


window.updateAdminUserStatus =
    updateAdminUserStatus;


window.getAdminRooms =
    getAdminRooms;


window.createAdminRoom =
    createAdminRoom;


window.assignStudentToRoom =
    assignStudentToRoom;


window.removeStudentFromRoom =
    removeStudentFromRoom;