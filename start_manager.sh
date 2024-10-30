#!/bin/bash

DJANGO_PID_FILE="/var/run/gunicorn.pid"
CONVERTER_PID_FILE="/var/run/converter.pid"
LOG_DIR="/var/log/smartlogger"
DJANGO_LOG_FILE="$LOG_DIR/gunicorn.log"
CONVERTER_LOG_FILE="$LOG_DIR/converter.log"
COLLECTSTATIC_LOG_FILE="$LOG_DIR/collectstatic.log"
VENV_DIR="/root/projects/django/django_smartlogger/env" # Caminho para seu ambiente virtual

# Função para registrar logs no formato correto
log_message() {
    local log_type=$1
    local log_title=$2
    local log_message=$3
    echo "$(date '+%Y-%m-%d %H:%M:%S')-$log_type-$log_title-$log_message" >> "$DJANGO_LOG_FILE"
}

# Função para verificar se o ambiente virtual está ativo
activate_venv() {
    if [ -d "$VENV_DIR" ]; then
        source "$VENV_DIR/bin/activate"
        log_message "INFO" "Django" "Virtual environment activated."
    else
        log_message "ERROR" "Django" "Virtual environment not found at $VENV_DIR"
        exit 1
    fi
}

start() {
    # Ativa o ambiente virtual
    activate_venv

    if [ ! -d "$LOG_DIR" ]; then
        mkdir -p "$LOG_DIR"
        log_message "INFO" "System" "Log directory created: $LOG_DIR"
    fi

    if [ ! -f "$DJANGO_LOG_FILE" ]; then
        touch "$DJANGO_LOG_FILE"
        log_message "INFO" "System" "Log file created: $DJANGO_LOG_FILE"
    fi

    if [ ! -f "$COLLECTSTATIC_LOG_FILE" ]; then
        touch "$COLLECTSTATIC_LOG_FILE"
        log_message "INFO" "System" "Collectstatic log file created: $COLLECTSTATIC_LOG_FILE"
    fi

    if [ -f "$DJANGO_PID_FILE" ]; then
        DJANGO_PID=$(cat "$DJANGO_PID_FILE")
        if ps -p "$DJANGO_PID" > /dev/null; then
            log_message "ERROR" "Django" "Gunicorn is already running (PID: $DJANGO_PID)."
            return 1
        else
            log_message "WARNING" "Django" "PID file exists but Gunicorn is not running. Removing stale PID file."
            rm -f "$DJANGO_PID_FILE"
        fi
    fi

    log_message "INFO" "Django" "Starting Gunicorn..."
    nohup gunicorn core.wsgi:application --bind 0.0.0.0:7000 --workers 3 --pid "$DJANGO_PID_FILE" > "$DJANGO_LOG_FILE" 2>&1 &
    sleep 3  # Espera alguns segundos para o Gunicorn iniciar
    if ps -p $(cat "$DJANGO_PID_FILE") > /dev/null; then
        log_message "INFO" "Django" "Gunicorn started with PID $(cat $DJANGO_PID_FILE)."
    else
        log_message "ERROR" "Django" "Gunicorn failed to start. Check logs."
        rm -f "$DJANGO_PID_FILE"
        return 1
    fi

    log_message "INFO" "Django" "Running collectstatic..."
    nohup python3 manage.py collectstatic --noinput > "$COLLECTSTATIC_LOG_FILE" 2>&1 &
    log_message "INFO" "Django" "Collectstatic completed."

    if [ -f "$CONVERTER_PID_FILE" ]; then
        CONVERTER_PID=$(cat "$CONVERTER_PID_FILE")
        if ps -p "$CONVERTER_PID" > /dev/null; then
            log_message "ERROR" "Converter" "Converter script is already running (PID: $CONVERTER_PID)."
            return 1
        else
            log_message "WARNING" "Converter" "PID file exists but converter is not running. Removing stale PID file."
            rm -f "$CONVERTER_PID_FILE"
        fi
    fi

    log_message "INFO" "Converter" "Starting converter script..."
    nohup python3 /root/projects/django/django_smartlogger/api/monitor/converter.py >> "$CONVERTER_LOG_FILE" 2>&1 &
    echo $! > "$CONVERTER_PID_FILE"
    log_message "INFO" "Converter" "Converter script started with PID $(cat $CONVERTER_PID_FILE)."
}

stop() {
    if [ -f "$DJANGO_PID_FILE" ]; then
        DJANGO_PID=$(cat "$DJANGO_PID_FILE")
        if ps -p "$DJANGO_PID" > /dev/null; then
            log_message "INFO" "Django" "Stopping Gunicorn (PID: $DJANGO_PID)..."
            kill "$DJANGO_PID"
            rm -f "$DJANGO_PID_FILE"
            log_message "INFO" "Django" "Gunicorn stopped."
        else
            log_message "WARNING" "Django" "Django PID file exists but no such process is running. Removing stale PID file."
            rm -f "$DJANGO_PID_FILE"
        fi
    else
        log_message "ERROR" "Django" "Gunicorn is not running."
    fi

    if [ -f "$CONVERTER_PID_FILE" ]; then
        CONVERTER_PID=$(cat "$CONVERTER_PID_FILE")
        if ps -p "$CONVERTER_PID" > /dev/null; then
            log_message "INFO" "Converter" "Stopping converter script (PID: $CONVERTER_PID)..."
            kill "$CONVERTER_PID"
            rm -f "$CONVERTER_PID_FILE"
            log_message "INFO" "Converter" "Converter script stopped."
        else
            log_message "WARNING" "Converter" "Converter PID file exists but no such process is running. Removing stale PID file."
            rm -f "$CONVERTER_PID_FILE"
        fi
    else
        log_message "ERROR" "Converter" "Converter script is not running."
    fi
}

restart() {
    stop
    start
}

status() {
    if [ -f "$DJANGO_PID_FILE" ]; then
        DJANGO_PID=$(cat "$DJANGO_PID_FILE")
        if ps -p "$DJANGO_PID" > /dev/null; then
            log_message "INFO" "Status" "Gunicorn is running (PID: $DJANGO_PID)."
        else
            log_message "ERROR" "Status" "Gunicorn PID file exists but the process is not running."
        fi
    else
        log_message "ERROR" "Status" "Gunicorn is not running."
    fi

    if [ -f "$CONVERTER_PID_FILE" ]; then
        CONVERTER_PID=$(cat "$CONVERTER_PID_FILE")
        if ps -p "$CONVERTER_PID" > /dev/null; then
            log_message "INFO" "Status" "Converter script is running (PID: $CONVERTER_PID)."
        else
            log_message "ERROR" "Status" "Converter PID file exists but the process is not running."
        fi
    else
        log_message "ERROR" "Status" "Converter script is not running."
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
