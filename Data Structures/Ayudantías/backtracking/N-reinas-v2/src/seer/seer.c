#include <gtk/gtk.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>

#include "../puzzle/cell_type.h"

/** Size in pixels of our basic grid square */
#define CELL_SIZE 48
/** Space between blocks to separate them */
#define SEPARATION 5

pthread_t *update_thread;

/** Width of our matrix */
uint8_t width;
/** Height of our matrix */
uint8_t height;
/** Matrix to keep track of the state of the board */
CellType **board;

/** Pointers to images that are the empty spaces */
cairo_surface_t **queen_sprite;

/** Arrays used to store the empty spaces displayed on the board */
cairo_surface_t **empty_sprite;


/** Helper method to draw the magnets and empty spaces */
void cairo_draw_cell(cairo_t *cr, CellType cell, int x, int y)
{
	double pos_x = x * CELL_SIZE + (x + 1) * SEPARATION + CELL_SIZE;
	double pos_y = y * CELL_SIZE + (y + 1) * SEPARATION + CELL_SIZE;
	switch (cell)
	{
	case EMPTY:
		cairo_set_source_surface(cr, empty_sprite[(x + y) % 2], pos_x, pos_y);
		break;
	case QUEEN:
		cairo_set_source_surface(cr, queen_sprite[(x + y) % 2], pos_x, pos_y);
		break;
	default:
		return;
	}
	cairo_paint(cr);
}

/** Renders all the elements on the screen */
gboolean draw(GtkWidget *widget, cairo_t *cr, gpointer data)
{
	/* Color of the background is 7C7062 Hex Color | RGB: 124, 112, 98 */
	cairo_set_source_rgb(cr, 124.0 / 255.0, 112.0 / 255.0, 98.0 / 255.0);
	cairo_paint(cr);

	/* We draw the magnets and the empty spaces */
	for (int row = 0; row < height; row++)
	{
		for (int col = 0; col < width; col++)
		{
			cairo_draw_cell(cr, board[row][col], col, row);
		}
	}

	return TRUE;
}

/** Method that recieves STDIN input from solver and updates the board acordingly */
void *update(void *canvas)
{
	uint8_t row, col;
	CellType val;
	char command[16];

	while (true)
	{
		/* We run the program until we recieve an end command or an invalid one */
		if (fscanf(stdin, "%s", command))
		{
			if (!strcmp(command, "END"))
			{
				gtk_main_quit();
				break;
			}
			else if (!strcmp(command, "CELL"))
			{
				if (!fscanf(stdin, "%hhu", &row))
					break;
				if (!fscanf(stdin, "%hhu", &col))
					break;
				if (!fscanf(stdin, "%u", &val))
					break;
				board[row][col] = val;
			}
			else
			{
				break;
			}
		}
		else
		{
			break;
		}
		gtk_widget_queue_draw(canvas);
	}
	pthread_exit(NULL);
}

/** Initialize the thread that will run the image */
void spawn_updater(GtkWidget *widget, gpointer user_data)
{
	/* Create the thread */
	update_thread = malloc(sizeof(pthread_t));
	/* Execute the thread */
	pthread_create(update_thread, NULL, update, widget);
}

/** Init our board with its default values and assign the pointers */
void matrix_init()
{
	empty_sprite = malloc(sizeof(cairo_surface_t *) * 2);
	empty_sprite[0] = cairo_image_surface_create_from_png("assets/empty_0.png");
	empty_sprite[1] = cairo_image_surface_create_from_png("assets/empty_1.png");

	queen_sprite = malloc(sizeof(cairo_surface_t *) * 2);
	queen_sprite[0] = cairo_image_surface_create_from_png("assets/queen_0.png");
	queen_sprite[1] = cairo_image_surface_create_from_png("assets/queen_1.png");

	board = malloc(sizeof(CellType *) * height);
	for (int row = 0; row < height; row++)
	{
		board[row] = malloc(sizeof(CellType) * width);

		for (int col = 0; col < width; col++)
		{
			board[row][col] = EMPTY;
		}
	}
}
/** Release all our memmory */
void matrix_destroy()
{
	/** Free our spirtes */
	free(empty_sprite);
	free(queen_sprite);

	for (int row = 0; row < height; row++)
	{
		free(board[row]);
	}
	free(board);
}

bool check_parameters(int argc, char **argv)
{
	if (argc != 3)
		return false;
	return true;
}

/** Visualize the image created by the renderer */
int main(int argc, char **argv)
{
	/* Check that our params are correct */
	if (!check_parameters(argc, argv))
		return 1;

	/* Load the puzzle */
	width = atoi(argv[1]);
	height = atoi(argv[2]);

	matrix_init();

	/* We close the GTK channel so that it doesn't cause trouble */
	fclose(stderr);

	/* Initialize GTK */
	gtk_init(0, NULL);

	/* Create the window */
	GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
	g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

	/* Create the canvas */
	GtkWidget *canvas = gtk_drawing_area_new();

	/* Set dimensions of the Canvas */
	double window_width = (CELL_SIZE + SEPARATION) * width + SEPARATION + 2 * (CELL_SIZE + SEPARATION);
	double window_height = (CELL_SIZE + SEPARATION) * height + SEPARATION + 2 * (CELL_SIZE + SEPARATION);

	gtk_widget_set_size_request(canvas, window_width, window_height);

	/* Link events to the method to our canvas */
	g_signal_connect(canvas, "draw", G_CALLBACK(draw), NULL);
	g_signal_connect(canvas, "realize", G_CALLBACK(spawn_updater), NULL);

	/* Insert the canvas in the window */
	gtk_container_add(GTK_CONTAINER(window), canvas);

	/* Show everything */
	gtk_widget_show(canvas);
	gtk_widget_show(window);

	/* Restart the execution of GTK */
	gtk_main();

	free(update_thread);
	matrix_destroy();

	return 0;
}
