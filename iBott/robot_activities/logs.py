import asyncio


class Log:
    """
    This class is used to log messages in the Orchestrator console.
    Arguments:
        connection: Connection instance to orchestrator.
    Attributes:
        connection: Connection instance to orchestrator.
    Methods:
        debug(log): Debug log.
        trace(log): Trace log.
        info(log): Info log.
        system_exception(error): System exception.
        business_exception(error): Business exception.
    """

    def __init__(self, connection):
        self.connection = connection

    def debug(self, log: str):
        """
        Send debug trace to the robot manager console.
        Arguments:
            log: The log message.
        Returns:
            None
        """
        log_type = 'debug'
        self.send(log, log_type=log_type)

    def trace(self, log: str):
        """
        Send trace to the robot manager console.
        Arguments:
            log: The log message.
        Returns:
            None
        """
        log_type = 'trace'
        asyncio.run(self.send(log, log_type=log_type))

    def info(self, log: str):
        """
        Send info trace to the robot manager console.
        Arguments:
            log: The log message.
        Returns:
            None
        """
        log_type = 'info'
        asyncio.run(self.send(log, log_type=log_type))

    def system_exception(self, error: str):
        """
        Send systemException trace to the robot manager console.
        Arguments:
            error: The error message.
        """
        log_type = 'systemException'
        asyncio.run(self.send(error, log_type=log_type))

    def business_exception(self, error: str):
        """
        Send businessException trace to orchestrator
        Arguments:
            error: The error message.
        """
        log_type = 'businessException'
        asyncio.run(self.send(error, log_type=log_type))

    async def send(self, log: str, log_type: str):
        """
        Async function to send logs to orchestrator
        Arguments:
            log: The log message.
            log_type: The log type.
        Raise:
            OrchestratorConnectionError: If the connection with the orchestrator is not established.
        """
        if not self.connection.debug:
            try:
                await self.connection.send_message(log, log_type=log_type)
            except:
                raise Exception("Orchestrator is not connected")
        else:
            print(f'{log_type}: {log}')
