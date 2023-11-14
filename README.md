<h1>Spinjrock's Custom KOTH Documentation</h1>
<h3>What do we need</h3>
<ol>
    <li>8 Boxes</li>
    <li>Network Gateway</li>
    <li>VPN into the network?</li>
    <li>If not VPN then attacker boxes on the network</li>
    <li>Scoring Engine</li>
    <li>Scoring Agents</li>
</ol>
<p>I'll be writing this in python, because it needs to be easy to maintain for those who come after me.</p>

<h3>Scoring Engine Design</h3>
    <h4>Website Front End</h4>
    <ol>
        <li>Shows current state of machines, and a leaderboard of teams/players</li>
    </ol>
    <h4>Back End</h4>
    <ol>
        <li>Recieves data about the state of the machines over udp/50435</li>
            <ol>
                <li>Probably does this using good old json and sockets</li>
            </ol>
        <li>Updates front end of the site</li>
    </ol>
<h3>Scoring Agent Design</h3>
    <ol>
        <li>Sends out status data to scoring agent server</li>
        <li>Looks for signs of ownership</li>
    </ol>
<h3>Box Design</h3>

<h3>Above and Beyond</h3>
<ol>
    <li>Implementation for network recognization and setup</li>
    <li>Hotswapping boxes</li>
    <li>Encrypted communication to the scoring engine</li>
    <li>Allow control of the machines via the scoring agent for administration purposes</li>
</ol>