// const express = require("express");
// const mongoose = require("mongoose");
// const { MongoClient } = require("mongodb");
// const app = express();
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const { MongoClient } = require("mongodb");
var bodyParser = require("body-parser");
const router = express.Router();

const app = express();
app.use(express.json());
// app.use(express.urlencoded());
app.use(cors());
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
);

// First MongoDB database
// const nflDBConnection = mongoose.createConnection(
//   "mongodb+srv://nicholasch24:hunter1224@cluster0.uuyxsu9.mongodb.net/nfl",
//   {
//     useNewUrlParser: true,
//     useUnifiedTopology: true,
//   }
// );
const nflDBConnection =
  "mongodb+srv://nicholasch24:hunter1224@cluster0.uuyxsu9.mongodb.net/nfl";
// Define a schema and model for the first database
const nflTeamDBSchema = new mongoose.Schema(
  {
    name: String,
  },
  { collection: "teams" }
);
const nflTeamDBModel = nflDBConnection.model("teams", nflTeamDBSchema);

const nflPlayerDBSchema = new mongoose.Schema(
  {
    name: String,
  },
  { collection: "players" }
);
// const nflClient = new MongoClient(nflDBConnection);
mongoose.connect(nflDBConnection).catch((err) => console.log(err));
const nflPlayerDBModel = nflDBConnection.model("players", nflPlayerDBSchema);

// Second MongoDB database
const nbaDBConnection = mongoose.createConnection(
  "mongodb+srv://nicholasch24:hunter1224@cluster0.uuyxsu9.mongodb.net/nba",
  {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  }
);

// Define a schema and model for the second database
const nbaTeamDBSchema = new mongoose.Schema(
  {
    title: String,
  },
  { collection: "NBAteamData" }
);
const nbaTeamDBModel = nbaDBConnection.model("NBAteamData", nbaTeamDBSchema);

const nbaPlayerDBSchema = new mongoose.Schema(
  {
    title: String,
  },
  { collection: "playerData" }
);
const nbaPlayerDBModel = nbaDBConnection.model(
  "NBAPlayerData",
  nbaPlayerDBSchema
);

// Route for getting data from the first database
app.get("/nfl/teams", async (req, res) => {
  const data = await nflTeamDBModel.find();
  res.json(data);
});

// app.route("/nfl/teams/:team_code").get(async (req, res) => {
//   const teamCode = req.params.team_code;
//   await Promise.all([
//     nflClient
//       .db("nfl")
//       .collection("teams")
//       .find({ team_code: teamCode })
//       .toArray(),
//     nflClient
//       .db("nfl")
//       .collection("playerData")
//       .find({ team_code: teamCode })
//       .toArray(),
//   ])
//     .then((values) => {
//       res.send([values[0], values[1]]);
//     })
//     .catch((error) => {
//       console.log(error);
//       res.send("Couldn't find");
//     });
//   // client.close();
// });

app.get("/nfl/players/:id", (req, res) => {
  nflPlayerDBModel.findById(req.params.id, (err, collection) => {
    if (err) return res.status(500).send(err);
    if (!collection) return res.status(404).send("No collection found.");
    res.send(collection);
  });
});

app.get("/nfl/players", async (req, res) => {
  const data = await nflPlayerDBModel.find();
  res.json(data);
});

// Route for getting data from the second database
app.get("/nba/players/:id", (req, res) => {
  nbaPlayerDBModel.findById(req.params.id, (err, collection) => {
    if (err) return res.status(500).send(err);
    if (!collection) return res.status(404).send("No collection found.");
    res.send(collection);
  });
});

app.get("/nba/teams", async (req, res) => {
  const data = await nbaTeamDBModel.find();
  res.json(data);
});
app.get("/nba/players", async (req, res) => {
  const data = await nbaPlayerDBModel.find();
  res.json(data);
});

app.get("/", (req, res) => {
  res.send("express in running");
});

// Start the server
app.listen(4000, () => {
  console.log("Server listening on port 4000");
});
