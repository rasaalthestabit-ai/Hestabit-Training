const mongoose = require("mongoose");
const bcrypt = require("bcrypt");

const AccountSchema = new mongoose.Schema(
{
    firstName: {
        type: String,
        required: true,
        trim: true
    },

    lastName: {
        type: String,
        required: true,
        trim: true
    },

    email: {
        type: String,
        required: true,
        unique: true,
        lowercase: true
    },

    password: {
        type: String,
        required: true,
        minlength: 6
    },

    status: {
        type: String,
        enum: ["active","inactive"],
        default: "active"
    }

},
{
    timestamps: true
}
);


AccountSchema.pre("save", async function(){

    if(!this.isModified("password")){
        return;
    }

    const hashedPassword = await bcrypt.hash(
        this.password,
        10
    );

    this.password = hashedPassword;

});


AccountSchema.virtual("fullName").get(function(){

    return this.firstName + " " + this.lastName;

});


AccountSchema.index({
    status:1,
    createdAt:-1
});


module.exports = mongoose.model(
    "Account",
    AccountSchema
);
