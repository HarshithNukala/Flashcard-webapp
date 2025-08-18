const authRegister = (req, res) => {
    res.json("Register an account.")
}

const authLogin = (req, res) => {
    res.json("Login to an account.")
}

export {
    authRegister,
    authLogin
}