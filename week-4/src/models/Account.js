const mongoose = require("mongoose");
const bcrypt = require("bcrypt");

const accountSchema = new mongoose.Schema(
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
    lowercase: true,
    trim: true
  },

  password: {
    type: String,
    required: true,
    minlength: 6
  },

  status: {
    type: String,
    enum: ["active", "inactive"],
    default: "active"
  },

  createdAt: {
    type: Date,
    default: Date.now
  }

},
{
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});


/*
Pre-save hook (Password hashing)
*/

accountSchema.pre("save", async function () {

  if (!this.isModified("password")) {
    return;
  }

  const salt = await bcrypt.genSalt(10);

  this.password = await bcrypt.hash(this.password, salt);

});


/*
Virtual Field
*/

accountSchema.virtual("fullName").get(function(){

return `${this.firstName} ${this.lastName}`;

});


/*
Compound Index
*/

accountSchema.index({
status: 1,
createdAt: -1
});


/*
TTL Index
*/

accountSchema.index(
{ createdAt: 1 },
{
expireAfterSeconds: 2592000,
partialFilterExpression: {
status: "inactive"
}
}
);


module.exports = mongoose.model("Account", accountSchema);