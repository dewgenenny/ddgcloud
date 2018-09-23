# docker_gcloud_dns
Gcloud DNS based dynamic DNS updater - checks your public IP then updates your gcloud DNS entries to match.

Requires two input files - hostlist should contain a list of the fully qualified domain names you'd like to update and client_secrets.json which contains the gcloud service accout details which are needed to update DNS entries in your gcloud account.

Also includes a dockerfile which you can use to build a docker image.

The docker image expects you to mount a file in /hostlist that contains a list of fully qualified domain names. Also requires a client_secrets.json file with a gcloud service account that has the right to change DNS entries for you..

example command: 

docker run --rm -v /home/user/ddgcloud/hostlist:/hostlist -v /home/user/ddgcloud/client_secrets.json:/client_secrets.json <image name>


Link to gcloud documentation around creating a service account: 

https://cloud.google.com/genomics/docs/how-tos/getting-started
