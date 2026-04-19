module.exports = {
  apps: [{
    name: "harmonica-app",
    script: "node_modules/.bin/next",
    args: "start -p 5123",
    cwd: "/var/www/harmonica-app",
    env: {
      NODE_ENV: "production",
    },
  }],
};
