#!/bin/sh

bot=false
server=false
worker=false


if [ $# -eq 0 ]; then
    echo "No arguments provided. Defaulting to running the server."
    bot=true
else
    bot=false
fi

export PROJECT_NAME=ohota_na_skidki_bot

while getopts ":bsw" option; do
    case "${option}" in
        b)
            bot=true
            ;;
        s)
            server=true
            ;;
        w)
            worker=true
            ;;
        *)
            echo "Invalid option: -$OPTARG" >&2
            ;;
    esac
done
shift $((OPTIND - 1))

python manage.py migrate

if [ "$bot" = true ]; then
    python manage.py migrate
    python manage.py start_bot
elif [ "$server" = true ]; then
    python manage.py collectstatic --noinput
    gunicorn ${PROJECT_NAME}.wsgi:application -c deployment/gunicorn.config.py --bind 0.0.0.0:80 --workers 3 --threads 2 --reload
elif [ "$worker" = true ]; then
    python manage.py qcluster
fi
