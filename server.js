const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const { MongoClient } = require("mongodb");
var bodyParser = require("body-parser");
const router = express.Router();

const app = express();
app.use(express.json());
app.use(express.urlencoded());
app.use(cors());
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
);

const uri =
  "mongodb+srv://nicholasch24:hunter1224@cluster0.uuyxsu9.mongodb.net/nfl";

const uriNBA =
  "mongodb+srv://nicholasch24:hunter1224@cluster0.uuyxsu9.mongodb.net/nba";

const client = new MongoClient(uri);
mongoose.connect(uri).catch((err) => console.log(err));

const NBAclient = new MongoClient(NBAuri);
mongoose.connect(NBAuri).catch((err) => console.log(err));

const playerSchema = mongoose.Schema(
  {
    name: String,
    team: String,
  },
  { collection: "playerData" }
);
const teamSchema = mongoose.Schema({
  name: String,
  rating: Number,
});

const Player = mongoose.model("playersData", playerSchema);
const Team = mongoose.model("teams", teamSchema);
const playerDetail = client.db("nfl").collection("playerData");

const NBAplayerDetail = NBAclient.db("nba").collection("playerData");
const NBAteamDetail = NBAclient.db("nba").collection("teamData");

const NBAplayerSchema = mongoose.Schema(
  {
    name: String,
    team: String,
  },
  { collection: "playerData" }
);
const NBAteamSchema = mongoose.Schema(
  {
    name: String,
  },
  { collection: "teamData" }
);
const NBAPlayer = mongoose.model("playerData", NBAplayerSchema);
const NBATeam = mongoose.model("teamData", NBAteamSchema);

app.get("/nba/teams", (req, res) => {
  NBATeam.find()
    .then((items) => res.json(items))
    .catch((err) => console.log(err));
});

async function findOneListingByName(client, playerId) {
  const result = await Player.findById({ name: playerId });

  if (result) {
    console.log(
      `Found a listing in the collection with the name '${playerId}':`
    );
    console.log(result);
  } else {
    console.log(`No listings found with the name '${playerId}'`);
  }
}

app.get("/players", (req, res) => {
  Player.find()
    .then((items) => res.json(items))
    .catch((err) => console.log(err));
});

app.get("/p/:id", (req, res) => {
  Player.findById(req.params.id, (err, collection) => {
    if (err) return res.status(500).send(err);
    if (!collection) return res.status(404).send("No collection found.");
    res.send(collection);
  });
});

app.get("/teams", (req, res) => {
  Team.find()
    .then((items) => res.json(items))
    .catch((err) => console.log(err));
});

app.route("/teams/:team_code").get(async (req, res) => {
  const teamCode = req.params.team_code;
  await Promise.all([
    client
      .db("nfl")
      .collection("teams")
      .find({ team_code: teamCode })
      .toArray(),
    client
      .db("nfl")
      .collection("playerData")
      .find({ team_code: teamCode })
      .toArray(),
  ])
    .then((values) => {
      res.send([values[0], values[1]]);
    })
    .catch((error) => {
      console.log(error);
      res.send("Couldn't find");
    });
  // client.close();
});

app.get("/", (req, res) => {
  res.send("express is here");
});

app.listen(5050, () => {
  console.log("Listening on 5050!");
});
